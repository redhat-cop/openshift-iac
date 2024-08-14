# Setup role

This role prepare the environment for the installation of the Openshift.

This role download and install following binaries:
 - openshift-install
 - oc

Downloads `oc` binary from official Openshift website. Then based on the input parameters
it either download `openshift-install` binary or extract it from the container `registry`.

This role also uses pip and system package manager to install following packages:

System dependencies:
    - podman
    - python3-hvac
    - python3-passlib
    - python3-pip
    - python3-kubernetes
    - python3-netaddr
    - python3-aiohttp

Pip dependencies:
 - infoblox-client (infoblox)

Note that `infoblox-client` is not provided via RPM, that is the reason we don't use RPM.

## Variables documentation

URL of client tools - `oc` and `openshift-install`.
Default is https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp
```yaml
setup_clients_url
```

The cluster name. Required.
```yaml
setup_cluster_name
```

Directory where downloaded binaries are stored.
Default is $HOME/{{ setup_cluster_name }}
```yaml
setup_binaries_dir
```

If `true` the `setup_binaries_dir` directory will be cleaned before role is executed.
```yaml
setup_binaries_clean
```

Version of the Openshift tools to be downloaded from the `setup_clients_url`.
Could be `latest`/`stable` or specific release.
```yaml
setup_cluster_version
```

If `true` custom registry is used and the `setup` role won't download `openshift-install`
binary from `setup_clients_url` URL. Default is `false`.
```yaml
setup_install_registry
```
