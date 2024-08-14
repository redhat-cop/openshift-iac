from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import re
import urllib.parse

from ansible.module_utils.urls import open_url
from ansible_collections.infoblox.nios_modules.plugins.module_utils.api import WapiLookup
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import open_session


class FilterModule(object):

    def filters(self):
        'Define filters'
        return {
            'fetch_ips': self.fetch_ips,
            'fetch_macaddrs': self.fetch_macaddrs,
            'merge_ips': self.merge_ips,
            'network_cidr': self.network_cidr,
            'worker_nodes_len': self.worker_nodes_len,
            'master_nodes_len': self.master_nodes_len,
            'vm_ids': self.vm_ids,
            'cluster_base_version': self.cluster_base_version,
            'product_release_version': self.product_release_version,
            'combine_pull_secret': self.combine_pull_secret,
            'create_pull_secret': self.create_pull_secret,
            'vsphere_nics': self.vsphere_nics,
        }

    def vsphere_nics(self, networks):
        # Takes as input openshift_install_network variable
        # and convert it to vsphere vm module nics parameter
        #
        ret = []
        for n in networks:
            nic = {}
            nic['mac_type'] = 'MANUAL' if n.get('macaddr') else 'GENERATED'
            nic['start_connected'] = True
            if n.get('macaddr'):
                nic['mac_address'] = n['macaddr']
            nic['backing'] = {}
            nic['backing']['type'] = 'DISTRIBUTED_PORTGROUP'
            nic['backing']['network'] = n['network']
            ret.append(nic)
        return ret

    def create_pull_secret(self, pull_secret, host, creds, email):
        return {"auths": {host: {"auth": creds, "email": email}}}

    def combine_pull_secret(self, pull_secret, host, creds, email):
        pull_secret["auths"].update({host: {"auth": creds, "email": email}})
        return json.dumps(pull_secret)

    def fetch_ips(self, nodes, cl_name, domain_name, **kwargs):
        provider = kwargs.pop('provider', {})
        wapi = WapiLookup(provider)

        ret = []
        for n in nodes:
            ip = wapi.get_object('record:a', {'name': n['name'] + '.' + cl_name + '.' + domain_name})
            if ip:
                n['ipaddr'] = ip[0]['ipv4addr']
            ret.append(n)
        return ret

    def cluster_base_version(self, cluster_version):
        """
        Get Openhsift base version based on cluster version

        :param cluster_version: Version of openshift
        """
        # Possible inputs:
        # 4.10.28
        # stable-4.9
        # latest-4.11
        # ...

        if 'latest' in cluster_version or 'stable' in cluster_version:
            cluster_base_version = cluster_version.split('-')[1]
        else:
            version_split = cluster_version.split('.')
            cluster_base_version = version_split[0] + '.' + version_split[1]
        return cluster_base_version

    def product_release_version(self, cluster_version):
        """
        Get the product release version based on cluster version (ie latest-4.10)

        :param openshift_version: Version of openshift to get OVA
        """
        clients_content = "https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/{0}/sha256sum.txt".format(cluster_version)

        response = open_url(clients_content)
        content = response.read().decode('utf-8')

        # openshift-install-linux - must be always there, so find its version:
        version_pattern = r"openshift-install-linux-(\d+\.\d+\.\d+)\.tar\.gz"

        matches = re.findall(version_pattern, content)

        for match in matches:
            return match

    def vm_ids(self, nodes, cl_name, **kwargs):
        self._vm_ids = []

        import asyncio

        current_loop = asyncio.get_event_loop_policy().get_event_loop()
        current_loop.run_until_complete(self.__fetch_vm_ids(nodes, cl_name, **kwargs))

        return self._vm_ids

    async def __fetch_vm_ids(self, nodes, cl_name, **kwargs):
        for node in nodes:
            session = await self.__get_session(**kwargs)
            role = node.get('role', 'master')
            vm_id = await self._fetch_vm_id(session, cl_name + '-' + role + '-' + node['name'], kwargs.get('vcenter_hostname'))
            if vm_id:
                self._vm_ids.append(vm_id)

    def master_nodes_len(self, nodes):
        return len([node for node in nodes if node.get('role', 'master') == 'master'])

    def worker_nodes_len(self, nodes):
        return len([node for node in nodes if node.get('role') == 'worker'])

    def network_cidr(self, network):
        n = network.split('/')
        if n > 1:
            return n[1]

    def merge_ips(self, openshift_nodes, ips):
        _openshift_nodes = []
        for idx, node in enumerate(openshift_nodes):
            node['ipaddr'] = ips[idx]
            _openshift_nodes.append(node)

        return _openshift_nodes

    def fetch_macaddrs(self, openshift_nodes, cl_name, **kwargs):
        """
        Update openshift_nodes variable with mac addresses fetch from VMware vCenter

        :param openshift_nodes: List of VM names to fetch mac addresses for
        """
        self._openshift_nodes = []
        import asyncio

        current_loop = asyncio.get_event_loop_policy().get_event_loop()
        current_loop.run_until_complete(self._fetch_macs(openshift_nodes, cl_name, **kwargs))

        return self._openshift_nodes

    async def _fetch_macs(self, openshift_nodes, cl_name, **kwargs):
        for vm in openshift_nodes:
            role = vm.get('role', 'master')
            mac = await self._fetch_mac(cl_name + '-' + role + '-' + vm['name'], **kwargs)
            if mac:
                vm['macaddr'] = mac
            self._openshift_nodes.append(vm)

    async def _fetch_mac(self, vm, **kwargs):
        vcenter_hostname = kwargs.get('vcenter_hostname')
        session = await self.__get_session(**kwargs)

        # Fetch vm id
        vm_id = await self._fetch_vm_id(session, vm, vcenter_hostname)
        if vm_id is None:
            return

        # Fetch nic id
        async with session.get("https://{0}/api/vcenter/vm/{1}/hardware/ethernet/".format(vcenter_hostname, vm_id)) as resp:
            _json = await resp.json()
            if len(_json) > 0 and 'nic' in _json[0]:
                nic = _json[0]['nic']
            else:
                return

        # Fetch nic mac address
        async with session.get("https://{0}/api/vcenter/vm/{1}/hardware/ethernet/{2}".format(vcenter_hostname, vm_id, nic)) as resp:
            _json = await resp.json()
            return _json['mac_address']

    async def _fetch_vm_id(self, session, vm, vcenter_hostname):
        # Fetch vm id
        vm_encode = '?names=' + urllib.parse.quote(vm)
        async with session.get("https://{0}/api/vcenter/vm{1}".format(vcenter_hostname, vm_encode)) as resp:
            _json = await resp.json()
            if len(_json) > 0 and 'vm' in _json[0]:
                return _json[0]['vm']

    async def __get_session(self, **kwargs):
        return await open_session(
            vcenter_hostname=kwargs.get('vcenter_hostname'),
            vcenter_username=kwargs.get('vcenter_username'),
            vcenter_password=kwargs.get('vcenter_password'),
            validate_certs=kwargs.get('vcenter_validate_certs', False),
        )

    async def __get_session_o(self, **kwargs):
        creds = get_credentials(**kwargs)
        return await open_session(
            vcenter_hostname=creds.get('vcenter_hostname'),
            vcenter_username=creds.get('vcenter_username'),
            vcenter_password=creds.get('vcenter_password'),
            validate_certs=creds.get('vcenter_validate_certs', False),
        )
