#!/usr/bin/python
REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = """
module: a10_slb_template_policy_class_list_lid
description:
    - Limit ID
author: A10 Networks 2018 
version_added: 1.8

options:
    
    lidnum:
        description:
            - Specify a limit ID
    
    conn-limit:
        description:
            - Connection limit
    
    conn-rate-limit:
        description:
            - Specify connection rate limit
    
    conn-per:
        description:
            - Per (Specify interval in number of 100ms)
    
    request-limit:
        description:
            - Request limit (Specify request limit)
    
    request-rate-limit:
        description:
            - Request rate limit (Specify request rate limit)
    
    request-per:
        description:
            - Per (Specify interval in number of 100ms)
    
    bw-rate-limit:
        description:
            - Specify bandwidth rate limit (Bandwidth rate limit in bytes)
    
    bw-per:
        description:
            - Per (Specify interval in number of 100ms)
    
    over-limit-action:
        description:
            - Set action when exceeds limit
    
    action-value:
        description:
            - 'forward': Forward the traffic even it exceeds limit; 'reset': Reset the connection when it exceeds limit; choices:['forward', 'reset']
    
    lockout:
        description:
            - Don't accept any new connection for certain time (Lockout duration in minutes)
    
    log:
        description:
            - Log a message
    
    interval:
        description:
            - Specify log interval in minutes, by default system will log every over limit instance
    
    direct-action:
        description:
            - Set action when match the lid
    
    direct-service-group:
        description:
            - Specify a service group (Specify the service group name)
    
    direct-pbslb-logging:
        description:
            - Configure PBSLB logging
    
    direct-pbslb-interval:
        description:
            - Specify logging interval in minutes(default is 3)
    
    direct-fail:
        description:
            - Only log unsuccessful connections
    
    direct-action-value:
        description:
            - 'drop': drop the packet; 'reset': Send reset back; choices:['drop', 'reset']
    
    direct-logging-drp-rst:
        description:
            - Configure PBSLB logging
    
    direct-action-interval:
        description:
            - Specify logging interval in minute (default is 3)
    
    response-code-rate-limit:
        
    
    dns64:
        
    
    uuid:
        description:
            - uuid of the object
    
    user-tag:
        description:
            - Customized tag
    

"""

EXAMPLES = """
"""

ANSIBLE_METADATA = """
"""

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["action_value","bw_per","bw_rate_limit","conn_limit","conn_per","conn_rate_limit","direct_action","direct_action_interval","direct_action_value","direct_fail","direct_logging_drp_rst","direct_pbslb_interval","direct_pbslb_logging","direct_service_group","dns64","interval","lidnum","lockout","log","over_limit_action","request_limit","request_per","request_rate_limit","response_code_rate_limit","user_tag","uuid",]

# our imports go at the top so we fail fast.
from a10_ansible.axapi_http import client_factory
from a10_ansible import errors as a10_ex

def get_default_argspec():
    return dict(
        a10_host=dict(type='str', required=True),
        a10_username=dict(type='str', required=True),
        a10_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=["present", "absent"])
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        
        action_value=dict(
            type='str' , choices=['forward', 'reset']
        ),
        bw_per=dict(
            type='int' 
        ),
        bw_rate_limit=dict(
            type='int' 
        ),
        conn_limit=dict(
            type='int' 
        ),
        conn_per=dict(
            type='int' 
        ),
        conn_rate_limit=dict(
            type='int' 
        ),
        direct_action=dict(
            type='bool' 
        ),
        direct_action_interval=dict(
            type='int' 
        ),
        direct_action_value=dict(
            type='str' , choices=['drop', 'reset']
        ),
        direct_fail=dict(
            type='bool' 
        ),
        direct_logging_drp_rst=dict(
            type='bool' 
        ),
        direct_pbslb_interval=dict(
            type='int' 
        ),
        direct_pbslb_logging=dict(
            type='bool' 
        ),
        direct_service_group=dict(
            type='str' 
        ),
        dns64=dict(
            type='str' 
        ),
        interval=dict(
            type='int' 
        ),
        lidnum=dict(
            type='int' , required=True
        ),
        lockout=dict(
            type='int' 
        ),
        log=dict(
            type='bool' 
        ),
        over_limit_action=dict(
            type='bool' 
        ),
        request_limit=dict(
            type='int' 
        ),
        request_per=dict(
            type='int' 
        ),
        request_rate_limit=dict(
            type='int' 
        ),
        response_code_rate_limit=dict(
            type='list' 
        ),
        user_tag=dict(
            type='str' 
        ),
        uuid=dict(
            type='str' 
        ), 
    ))
    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/slb/template/policy/{name}/class-list/lid/{lidnum}"
    f_dict = {}
    
    f_dict["lidnum"] = ""

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/slb/template/policy/{name}/class-list/lid/{lidnum}"
    f_dict = {}
    
    f_dict["lidnum"] = module.params["lidnum"]

    return url_base.format(**f_dict)


def build_envelope(title, data):
    return {
        title: data
    }

def build_json(title, module):
    rv = {}
    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v:
            rx = x.replace("_", "-")
            rv[rx] = module.params[x]
        # else:
        #     del module.params[x]

    return build_envelope(title, rv)

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if params.get(x)])
    
    errors = []
    marg = []
    
    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc,msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc,msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc,msg = REQUIRED_VALID
    
    if not rc:
        errors.append(msg.format(", ".join(marg)))
    
    return rc,errors

def exists(module):
    try:
        module.client.get(existing_url(module))
        return True
    except a10_ex.NotFound:
        return False

def create(module, result):
    payload = build_json("lid", module)
    try:
        post_result = module.client.post(new_url(module), payload)
        result.update(**post_result)
        result["changed"] = True
    except a10_ex.Exists:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def update(module, result):
    payload = build_json("lid", module)
    try:
        post_result = module.client.put(existing_url(module), payload)
        result.update(**post_result)
        result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def present(module, result):
    if not exists(module):
        return create(module, result)
    else:
        return update(module, result)

def absent(module, result):
    return delete(module, result)



def run_command(module):
    run_errors = []

    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    state = module.params["state"]
    a10_host = module.params["a10_host"]
    a10_username = module.params["a10_username"]
    a10_password = module.params["a10_password"]
    # TODO(remove hardcoded port #)
    a10_port = 443
    a10_protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        map(run_errors.append, validation_errors)
    
    if not valid:
        result["messages"] = "Validation failure"
        err_msg = "\n".join(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)

    if state == 'present':
        result = present(module, result)
    elif state == 'absent':
        result = absent(module, result)
    return result

def main():
    module = AnsibleModule(argument_spec=get_argspec())
    result = run_command(module)
    module.exit_json(**result)

# standard ansible module imports
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()