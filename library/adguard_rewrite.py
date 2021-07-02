
# Copyright: (c) 2021, Sebastian Sdorra <s.sdorra@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: adguard_rewrite

short_description: Manage AdGuard Home Rewrite Rules

version_added: "2.4"

description:
    - "Create, delete and update AdGuard Home Rewrite Rules"

options:
    path:
        description:
            - Path to Adguard Home config
        required: true
    domain:
        description:
            - Name of the domain
        required: true
    answer:
        description:
            - IPv4, IPv6 or CNAME Record
        required: true
    state:
        description:
            - State of rule present or absent
        required: true

author:
    - Sebastian Sdorra (@ssdorra)
'''

EXAMPLES = '''
# Add a rewrite rule
- name: Add a rewrite rule to config
  adguard_rewrite:
    path: /etc/adguard.yml
    domain: hello.example.net
    answer: 192.168.0.1
    state: present
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the test module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import yaml

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='path', required=True),
        domain=dict(type='str', required=True),
        answer=dict(type='str', required=True),
        state= dict(default='present', choices=['present', 'absent'])
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
        #original_message='',
        #message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )


    path = module.params['path']
    domain = module.params['domain']
    answer = module.params['answer']
    state = module.params['state']

    with open(path, 'r') as stream:
        adguard_config = yaml.safe_load(stream)

    if state == "present":

        if not 'rewrites' in adguard_config['dns']:
            adguard_config['dns']['rewrites'] = [{
                'domain': domain,
                'answer': answer
            }]
            result['changed'] = True
        else:
            found = False
            for entry in adguard_config['dns']['rewrites']:
                if entry['domain'] == domain and entry['answer'] == answer:
                    found = True
            if not found:
                adguard_config['dns']['rewrites'].append({
                    'domain': domain,
                    'answer': answer
                })
                result['changed'] = True
    else:
        entryToRemove = None
        for entry in adguard_config['dns']['rewrites']:
            if entry['domain'] == domain and entry['answer'] == answer:
                entryToRemove = entry
        if entryToRemove != None:
            adguard_config['dns']['rewrites'].remove(entryToRemove)
            result['changed'] = True


    if result['changed']:
        with open(path, 'w') as stream:
            yaml.dump(adguard_config, stream, default_flow_style=False, allow_unicode=True)

    
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    #result['original_message'] = module.params['name']
    #result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    #if module.params['new']:
    #    result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    #if module.params['name'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()