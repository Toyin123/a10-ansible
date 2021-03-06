#!/usr/bin/python
REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = """
module: a10_slb_template_cache
description:
    - RAM caching template
author: A10 Networks 2018 
version_added: 1.8

options:
    
    name:
        description:
            - Specify cache template name
    
    accept-reload-req:
        description:
            - Accept reload requests via cache-control directives in HTTP headers
    
    age:
        description:
            - Specify duration in seconds cached content valid, default is 3600 seconds (seconds that the cached content is valid (default 3600 seconds))
    
    default-policy-nocache:
        description:
            - Specify default policy to be to not cache
    
    disable-insert-age:
        description:
            - Disable insertion of age header in response served from RAM cache
    
    disable-insert-via:
        description:
            - Disable insertion of via header in response served from RAM cache
    
    max-cache-size:
        description:
            - Specify maximum cache size in megabytes, default is 80MB (RAM cache size in megabytes (default 80MB))
    
    min-content-size:
        description:
            - Minimum size (bytes) of response that can be cached - default 512
    
    max-content-size:
        description:
            - Maximum size (bytes) of response that can be cached - default 81920 (80KB)
    
    local-uri-policy:
        
    
    uri-policy:
        
    
    remove-cookies:
        description:
            - Remove cookies in response and cache
    
    replacement-policy:
        description:
            - 'LFU': LFU; choices:['LFU']
    
    logging:
        description:
            - Specify logging template (Logging Config name)
    
    verify-host:
        description:
            - Verify request using host before sending response from RAM cache
    
    uuid:
        description:
            - uuid of the object
    
    user-tag:
        description:
            - Customized tag
    
    sampling-enable:
        
    

"""

EXAMPLES = """
"""

ANSIBLE_METADATA = """
"""

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["accept_reload_req","age","default_policy_nocache","disable_insert_age","disable_insert_via","local_uri_policy","logging","max_cache_size","max_content_size","min_content_size","name","remove_cookies","replacement_policy","sampling_enable","uri_policy","user_tag","uuid","verify_host",]

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
        
        accept_reload_req=dict(
            type='bool' 
        ),
        age=dict(
            type='int' 
        ),
        default_policy_nocache=dict(
            type='bool' 
        ),
        disable_insert_age=dict(
            type='bool' 
        ),
        disable_insert_via=dict(
            type='bool' 
        ),
        local_uri_policy=dict(
            type='list' 
        ),
        logging=dict(
            type='str' 
        ),
        max_cache_size=dict(
            type='int' 
        ),
        max_content_size=dict(
            type='int' 
        ),
        min_content_size=dict(
            type='int' 
        ),
        name=dict(
            type='str' , required=True
        ),
        remove_cookies=dict(
            type='bool' 
        ),
        replacement_policy=dict(
            type='str' , choices=['LFU']
        ),
        sampling_enable=dict(
            type='list' 
        ),
        uri_policy=dict(
            type='list' 
        ),
        user_tag=dict(
            type='str' 
        ),
        uuid=dict(
            type='str' 
        ),
        verify_host=dict(
            type='bool' 
        ), 
    ))
    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/slb/template/cache/{name}"
    f_dict = {}
    
    f_dict["name"] = ""

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/slb/template/cache/{name}"
    f_dict = {}
    
    f_dict["name"] = module.params["name"]

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
    payload = build_json("cache", module)
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
    payload = build_json("cache", module)
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