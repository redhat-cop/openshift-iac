# Registry role

This role setup registry for restricted Openshfit installation, which don't have access to the internet.
If requested it generate new certificate via the certificate management system defined. It store the certificate
in the `{{ registry_directory }}/certs/` directory for later use by the other roles.

## Variables documentation

The cluster name. Required.
Required.
```registry_cluster_name```

Directory that contains `oc` binary file. Used to mirror the registry and extract `openshift-install` command.
Default `{{ ansible_env.HOME }}/.{{ registry_cluster_name }}/bin`.
```registry_binaries_dir```

Directory where certs and httpassd files are created for the registry and then mount to container.
Default `{{ ansible_env.HOME }}/.{{ registry_cluster_name }}/.registry`.
```registry_directory```

Define a username for the registry to be used for authentication.
Default `ansible`.
```registry_username```

Define a password for user specified in `registry_username`.
Default `ansible`.
```registry_password```

A port of the registry which should be exposed.
Default `5000`.
```registry_port```

A pull secret for the registry we want to mirror. Required.
```registry_pull_secret```

Define a repository which should be mirrored.
Default `openshift-release-dev`.
```registry_product_repo```

Default `ocp4/openshift4`.
```registry_repo```

Host of the registry. It's the current host the role is running on.
Default `ansible_hostname`.
```registry_host```

Registry release.
Default `ocp-release`.
```registry_release```

The version of the release.
Default `4.15.0-ec.2-x86_64`.
```registry_ocp_release```

The e-mail to be defined the in the pull secret of the created registry.
```registry_email```

The type of the certificate management system.
Default `vault`.
```registry_certificate_type```

When requesting certificate from certificate managment system this is value of certificate validity.
Default `1825d`.
```registry_certificate_ttl```

### Vault certificate management

Vault role to be used to generate the certificate.
```registry_vault_role_name```

URL of the vault system.
```registry_vault_url```

A token to authenticate to `vault` system.
```registry_vault_token```
