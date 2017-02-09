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

import keystoneclient.v2_0.client as ksclient
#from credentials import get_keystone_creds
#from credentials import get_heat_creds
from heatclient.client import Client

keystone = None
heat = None
stack_name = None

#keystone authentication
def auth_cloudify():
        try:
            print "authenticating to Cloudify"
            #Insert code
        except ValueError:
            print "Error authenticating to Cloudify"
        # Insert code


#Generate Stack name
def my_random_string_cloudify(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    global stack_name
    stack_name= 'nct_' + random[0:string_length]
    return random[0:string_length] # Return the random string.



#create Stack
def stack_create_cloudify(nct_template):
    auth_cloudify()
    my_random_string_cloudify()
    # Insert code



# Delete Stack
def stack_delete_cloudify(stack_uuid):
    auth_cloudify()
    # Insert code


# Status Stack
def stack_status_cloudify(stack_uuid):
    auth_cloudify()
    # Insert code

# Output Stack
def stack_output_cloudify(stack_uuid):
    auth_cloudify()
    # Insert code
