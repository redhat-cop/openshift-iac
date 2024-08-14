# Configure role

This role prepare the configuration of the openshift installation via openshift-install `agent` command.
For Vsphere we create vmware VMs we capture the MAC of the VMs and prepare the networking
configuration for `agent` installation.

## Parameters

List of dictionaries describing Openshift nodes.
```
configure_nodes {
  name[required] - Name of the node. Used as a prefix for VM.
  ipaddr - If specified IP will be reserved in the DDI system.
  macaddr - If specified MAC address will be set for the NIC of the VM.
  role - role of the node in Openshift. Either master or worker.
}
```

# VMWare spec

The name of the vCenter datacenter where VMs will be created. Required.
```configure_datacenter```

The name of the vCenter cluster where VMs will be created. Required.
```configure_cluster```

The name of the datastore to use for VMs disks. Required.
```configure_datastore```

Name of the network VMs network interface will be attached to. Required.
```configure_network_name```

Name of the folder where data of VMs are stored. Required.
```configure_folder```

Dictionary with Vsphere connection details. Required.
```
configure_vsphere {
    vcenter_hostname - Hostname of the Vcenter.
    vcenter_username - Vcenter username.
    vcenter_password - Vcenter password.
    vcenter_validate_certs - True if certificate should be validated.
}
```

Hardware version defines the valid virtual hardware versions for a virtual machine. See [Virtual machine hardware versions](https://kb.vmware.com/s/article/1003746). Default 'VMX_17'.
```configure_hardware_version```

# Resources spec
Memory size of master VMs. Default 32768 MiB.
```configure_master_mib```

Memory size of worker VMs. Default 32768 MiB.
```configure_worker_mib```

CPU cores for worker VMs. The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket. Default 6.
```configure_worker_cpu_count```

CPU cores per socket for worker VMs. The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket. Default 2.
```configure_worker_cpu_cps```

CPU cores for master VMs. The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket. Default 6.
```configure_master_cpu_count```

CPU cores per socket for master VMs. The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket. Default 2.
```configure_master_cpu_cps```

# Networking

Name of the network interface passed to nmstate. Default ens160.
```configure_interface_name```

Next hop address for the node traffic. This must be in the same subnet as the IP address set for the specified interface.
```configure_default_route```

Specifies the search and server settings for the DNS server.
```configure_dns_servers```

# Openshift spec

The cluster network provider Container Network Interface (CNI) plugin to install.
Either OpenShiftSDN or OVNKubernetes. OpenShiftSDN is a CNI provider for all-Linux networks. OVNKubernetes is a CNI provider for Linux networks and hybrid networks that contain both Linux and Windows servers. The default value is OpenShiftSDN.
```configure_network_type```

The IP address block for machines.
```configure_network```

The base domain of the cluster. All DNS records will be sub-domains of this base and include the cluster name. Required.
```configure_base_domain```

The cluster name. Required.
```configure_cluster_name```

The SSH key or keys to authenticate access your cluster machines.
```configure_ssh_key```

The [pull secret](https://console.redhat.com/openshift/install/pull-secret) from the Red Hat OpenShift Cluster Manager. This pull secret allows you to authenticate with the services that are provided by the included authorities, including Quay.io, which serves the container images for OpenShift Container Platform components.
```configure_pull_secret```

Whether to enable or disable FIPS mode. By default, FIPS mode is not enabled. If FIPS mode is enabled, the Red Hat Enterprise Linux CoreOS (RHCOS) machines that OpenShift Container Platform runs on bypass the default Kubernetes cryptography suite and use the cryptography modules that are provided with RHCOS instead. Default false.
```configure_fips```

# Binaries
Directory of binaries.
Default is $HOME/{{ configure_cluster_name }}/bin
```configure_binaries_dir```

Path of `openshift-install` binary.
Default {{ configure_binaries_dir }}/openshift-install.
```configure_install_binary```

# DHCP
If true Openshift machines will be configured to use DHCP for networking. Default false.
```configure_dhcp```

If true the IP address will be reserved in DHCP system. Default true.
```configure_dhcp_reservation```

Dictionary with DDI connection details. Required.
```
configure_dns_provider {
    host - Specifies the DNS host name or address for connecting to the remote instance DDI.
    username - Configures the username to use to authenticate the connection to the remote instance of DDI.
    password - Specifies the password to use to authenticate the connection to the remote instance of DDI.
}
```

Directory where temporary data of cluster are stored. Default $HOME/{{ configure_cluster_name }}.
```configure_cluster_home_dir```

# Registry
If custom registry is used those variables are used to modify the pull secret with custom registry credentials.

Registry CA cert.
```configure_registry_cert```

Path to directory which contains CA cert of the registry. It will be loaded to `configure_registry_cert` if not specicified.
```configure_registry_directory```

Registry username. Default ansible.
```configure_registry_username```

Registry password. Default ansible
```configure_registry_password```

Registry user's email.
```configure_registry_email```

Registry port. Default 5000.
```configure_registry_port```

Registry hostname. Default `ansible_hostname`.
```configure_registry_host```

Wait for `openshift-install` command to finish. Default true.
```configure_wait_for_install```