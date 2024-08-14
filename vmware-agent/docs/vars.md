## Required variables

### Common

The name of the cluster. Collection will create a subdomain with this name, and all DNS records in this sub-domain.
This name is also used as prefix for Vcenter/DNS/Load balancer records and cache directory.
```
openshift_install_cluster_name
```

List of dictionaries describing Openshift nodes.
```
openshift_install_nodes {
  name[required] - Name of the node. DNS records are created based on the name.
  ipaddr - If specified static IP configuration will be used for the node.
  macaddr - If specified MAC address will be reserved for the node.
}
```

### Vcenter variables

The name of the vCenter datacenter where VMs will be created.
```
openshift_install_vcenter_datacenter
```

The name of the vCenter cluster where VMs will be created.
```
openshift_install_vcenter_cluster
```

The name of the datastore to use for VMs disks.
```
openshift_install_vcenter_datastore
```

Name of the network VMs network interface will be attached to.
```
openshift_install_vcenter_network
```

Name of the folder where data of VMs are stored.
```
openshift_install_vcenter_folder
```

### Vcenter
### Load balancer
#### F5
### DDI

### IPAM

Network range that will be used to allocate addresses for Openshift nodes and used as Openshift machine network (eg 10.1.198.224/28).
```
openshift_install_network
```

The virtual IP (VIP) address that will be configured for control plane API access.
```
openshift_install_api_vip
```

The virtual IP (VIP) address that will be configured for cluster ingress.
```
openshift_install_ingress_vip
```

### DNS

The base domain of the cluster. All DNS records will be sub-domains of base domain and include the cluster name.
```
openshift_install_base_domain
```

#### Infoblox

DNS primary grid where the DNS zone will be created.
```
openshift_install_dns_primary_grid
```

### Openshift
