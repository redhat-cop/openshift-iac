# Baremetal role

This role prepare the baremetal configuration of the openshift installation via openshift-install `agent` command.

## Parameters

List of dictionaries describing Openshift nodes.
```
baremetal_nodes {
  name[required] - Name of the node. Used as a prefix for VM.
  ipaddr - If specified IP will be reserved in the DDI system.
  macaddr - If specified MAC address will be set for the NIC of the VM.
  role - role of the node in Openshift. Either master or worker.
  bmc_username - Username of the BMC host
  bmc_password - Password of the BMC host
  bmc_address - Address of the BMC host
}
```

Bare-metal machines often have more than one block device, and in many cases a user will want to specify, which of them to use as the root device. Root device hints allow selecting one device or a group of devices to choose from.
```baremetal_root_device_hints```

# Networking

Name of the network interface passed to nmstate. Default ens160.
```baremetal_interface_name```

Next hop address for the node traffic. This must be in the same subnet as the IP address set for the specified interface.
```baremetal_default_route```

Specifies the search and server settings for the DNS server.
```baremetal_dns_servers```

API virtual IP to be created for the Openshift installation.
```baremetal_api_vip```

API ingress IP to be created for the Openshift installation.
```baremetal_ingress_vip```

# Openshift spec

The cluster network provider Container Network Interface (CNI) plugin to install.
OVNKubernetes is a CNI plugin for Linux networks and hybrid networks that contain both Linux and Windows servers. The default value is OVNKubernetes.
```baremetal_network_type```

The IP address block for machines.
```baremetal_network```

The base domain of the cluster. All DNS records will be sub-domains of this base and include the cluster name. Required.
```baremetal_base_domain```

The cluster name. Required.
```baremetal_cluster_name```

The SSH key or keys to authenticate access your cluster machines.
```baremetal_ssh_key```

The [pull secret](https://console.redhat.com/openshift/install/pull-secret) from the Red Hat OpenShift Cluster Manager. This pull secret allows you to authenticate with the services that are provided by the included authorities, including Quay.io, which serves the container images for OpenShift Container Platform components.
```baremetal_pull_secret```

Whether to enable or disable FIPS mode. By default, FIPS mode is not enabled. If FIPS mode is enabled, the Red Hat Enterprise Linux CoreOS (RHCOS) machines that OpenShift Container Platform runs on bypass the default Kubernetes cryptography suite and use the cryptography modules that are provided with RHCOS instead. Default false.
```baremetal_fips```

# Binaries
Directory of binaries.
Default is $HOME/{{ baremetal_cluster_name }}/bin
```baremetal_binaries_dir```

Path of `openshift-install` binary.
Default {{ baremetal_binaries_dir }}/openshift-install.
```baremetal_install_binary```

# DHCP
If true Openshift machines will be configured to use DHCP for networking. Default false.
```baremetal_dhcp```