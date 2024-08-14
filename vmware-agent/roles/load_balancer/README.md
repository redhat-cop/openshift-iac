# Load balancer role

This role setup the load balancer[1] for Openshift.

Currently we support only BigIP F5.

[1] https://docs.openshift.com/container-platform/4.14/installing/installing_vsphere/installing-vsphere.html#installation-load-balancing-user-infra_installing-vsphere

## Parameters

Dictionary specyfing nodes to create LB records for.
```
load_balancer_nodes {
    name - name of the node. used as a prefix for LB records
    ipaddr - IP address of the node
    role - role of the node either worker or master
}
```

Cluster name. Used as prefix for LB records. **Required**.
```load_balancer_cluster_name```

The virtual IP (VIP) address that will be configured for control plane API access.
```load_balancer_api_vip```

The virtual IP (VIP) address that will be configured for cluster ingress.
```load_balancer_ingress_vip```

Dictionary that define a credentials to connect to the F5 system. **Required**.
```
load_balancer_provider {
   server - F5 server hostname
   user - Username of the user to use F5 system
   password - Password of the user speficied in user field
}
```