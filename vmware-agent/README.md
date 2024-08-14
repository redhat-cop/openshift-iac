[![Ansible Integration Test](https://github.com/machacekondra/openshift_install/actions/workflows/ansible-test-integration.yml/badge.svg?branch=main)](https://github.com/machacekondra/openshift_install/actions/workflows/ansible-test-integration.yml)

# Openshift install collection
This collection contains roles to install and configure Openshift and its infrastructure.
The collection contains roles to setup external DNS and LoadBalancer. It's using [agent based](https://docs.openshift.com/container-platform/4.14/installing/installing_with_agent_based_installer/installing-with-agent-based-installer.html)
installation method for Openshift.

## Infrastructure support

Openshift platforms:
  - vpshere
  - baremetal

DNS systems:
  - Infoblox

LoadBalancer systems:
  - F5

Certificate management systems:
  - HashiCorp Vault

## Requirements:
 - Python 3.8
 - Ansible 2.13

## Dependencies:
Following dependencies will be installed by collection on the node which is used for installation:

 - python3-aiohttp (vmware)
 - python3-hvac (hashi vault)
 - infoblox-client (infoblox)
 - nmstate (openshift-install agent)
 - openshift-install
 - oc

## Included content

### Roles
Name | Description
--- | ---
[machacekondra.openshfit_install.registry](https://github.com/machacekondra/openshift_install/blob/main/roles/registry/README.md)|Setup the custom containers registry which mirros the Openshift registry.
[machacekondra.openshfit_install.setup](https://github.com/machacekondra/openshift_install/blob/main/roles/setup/README.md)|Prepare the dependencies to run the installation.
[machacekondra.openshfit_install.dns](https://github.com/machacekondra/openshift_install/blob/main/roles/dns/README.md)|Configure the DNS for the Openshift nodes.
[machacekondra.openshfit_install.load_balancer](https://github.com/machacekondra/openshift_install/blob/main/roles/load_balancer/README.md)|Configure load balancer for API/Ingress for Openshift.
[machacekondra.openshfit_install.configure](https://github.com/machacekondra/openshift_install/blob/main/roles/configure/README.md)|Setup the nodes and run the installation of the Openshift.
[machacekondra.openshfit_install.post_install](https://github.com/machacekondra/openshift_install/blob/main/roles/post_install/README.md)|Run the post install tasks.

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the collection, you need to install it with the Ansible Galaxy CLI:

```bash
$ ansible-galaxy collection install machacekondra.openshift_install
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: machacekondra.openshift_install
    version: 0.0.1
```

### Using this collection

There are few mandatory variables which must be specified to configure the infrastructure.
All the variables are documented in specific roles and also [here](docs/vars.md).

## Execution

To run the playbook execute following command:

```bash
$ ansible-playbook -i ocp_prod machacekondra.openshift_install.run
```

Where the `ocp_prod` is inventory file, with specified variables for your infrastructure.
The example inventory files are in `examples` directory.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
