# Ansible Role for AdGuard Home

## Installation

Just clone the repository and add the library folder to the ansible module path.
For more information have a look at the [ansible documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#adding-a-module-locally).

## Usage

To add a rewrite rule to the AdGuard config:

```yaml
- name: Add a rewrite rule to config
  adguard_rewrite:
    path: adguard.yaml
    domain: hello.example.net
    answer: 192.168.0.1
```

To remove a rewrite rulr from the AdGuard config:
```yaml
- name: Remove a rewrite rule from config
  adguard_rewrite:
    path: adguard.yaml
    domain: hello.example.net
    answer: 192.168.0.1
    state: absent
```

## Example

Have a look at the [example playbook](examplepb.yaml)
