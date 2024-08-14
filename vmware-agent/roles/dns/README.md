# DNS role

This role setup the DNS[1] for Openshift.

Supported DNS systems:

 - Infoblox

This role follow following [guide](https://docs.openshift.com/container-platform/4.14/installing/installing_vsphere/installing-vsphere.html#installation-dns-user-infra_installing-vsphere) to configure all relevant DNS records:

## Parameters

Dictionary describing Openshift nodes.
```
dns_nodes {
    name - name of the machine DNS A record will be created.
}
```

The base domain of the cluster. Required.
```dns_base_domain```

The cluster name. Required.
```dns_cluster_name```

Network range that will be used to allocate addresses for Openshift nodes. **Required if** static IPs not provided.
```dns_network```

## Infoblox parameters

Dictionary that define a credentials to connect to the Infoblox system. **Required**.
```yaml
dns_provider {
 host - hostname of the Infoblox systme
 username - Username of the user to use Infoblox system
 password - Password of the user speficied in username
}
```

Primary grid for the DNS zone. **Required**.
```dns_primary_grid```

Network view of the DNS records. Default is `default`.
```dns_network_view```