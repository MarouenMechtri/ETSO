#  Copyright 2015-2016 Institut Mines-Telecom - Telecom SudParis
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Created on Sep 15, 2016
@authors: Marouen Mechtri, Chaima Ghribi
@contacts: {marouen.mechtri, chaima.ghribi}@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import logging.config
import os
import time
import sys
import json
import requests
import uuid
import yaml
import ast

import keystoneclient.v2_0.client as ksclient
from heatclient.client import Client

keystone = None
heat = None

#keystone authentication
def auth_heat(username, password, endpoint, tenant_name):
        try:
            keystone_client = ksclient.Client(username=username, password=password, auth_url=endpoint, project_name=tenant_name)
        except ValueError:
            print "Error authenticating to the keystone"
        global keystone
        keystone = keystone_client
        return keystone_client

#Connect to heat
def get_heat(heat_url):
    try:
        auth_token = keystone.auth_token
        heat_client = Client('1', endpoint=heat_url, token=auth_token)
    except ValueError:
        print "Error in connecting to heat"
    global heat
    heat = heat_client
    return heat_client


#Generate Stack name
def my_random_string_heat(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    global stack_name
    stack_name= 'nct_' + random[0:string_length]
    return random[0:string_length] # Return the random string.



#create Stack
def stack_create_heat(username, password, endpoint, tenant_name, heat_url, nct_template, stack_name):
    auth_heat(username, password, endpoint, tenant_name)
    get_heat(heat_url)
    #my_random_string_heat()
    #print nct_template
    stack = heat.stacks.create(stack_name=stack_name, template=nct_template, parameters={})

    stack_dict = heat.stacks.get(stack['stack']['id']).to_dict()

    #uid = stack['stack']['id']
    #global stack_uuid
    #stack_uuid=uid
    while stack_dict['stack_status'] == 'CREATE_IN_PROGRESS':
        print "Stack " + stack_name + " in state: {}".format(stack_dict['stack_status'])
        stack_dict = heat.stacks.get(stack['stack']['id']).to_dict()
        time.sleep(2)

    if stack_dict['stack_status'] == 'CREATE_COMPLETE':
        print "Stack succesfully created."



    return stack



# Delete Stack
def stack_delete_heat(username, password, endpoint, tenant_name, heat_url, stack_uuid):
    auth_heat(username, password, endpoint, tenant_name)
    get_heat(heat_url)
    while heat.stacks.get(stack_uuid).to_dict()['stack_status']!='DELETE_COMPLETE':
        if heat.stacks.get(stack_uuid).to_dict()['stack_status']=='DELETE_IN_PROGRESS':
            time.sleep(2)
        else:
            # in case of DELETE_FAILED or CREATE_COMPLETE
            print heat.stacks.get(stack_uuid).to_dict()['stack_status']
            heat.stacks.delete(stack_id=stack_uuid)
            time.sleep(2)

    print "Stack Released = " + stack_uuid



# Status Stack
def stack_status_heat(username, password, endpoint, tenant_name, heat_url, stack_uuid):
    auth_heat(username, password, endpoint, tenant_name)
    get_heat(heat_url)
    return heat.stacks.get(stack_uuid).to_dict()['stack_status']



# Output Stack
def stack_output_heat(username, password, endpoint, tenant_name, heat_url, stack_uuid, output_template):
    auth_heat(username, password, endpoint, tenant_name)
    get_heat(heat_url)

    stack_dict = heat.stacks.get(stack_uuid).to_dict()

    outputs = json.loads(output_template)

    stack_data = {}
    for output_file in outputs:
        stack_data[outputs[output_file]['value']['get_attr'][0]] = {}
        stack_data[outputs[output_file]['value']['get_attr'][0]]['name'] = output_file

        for output_stack in stack_dict.get('outputs', []):
            if output_stack['output_key'] == output_file:
                stack_data[outputs[output_file]['value']['get_attr'][0]][outputs[output_file]['value']['get_attr'][1]] = output_stack['output_value']

    return stack_data
