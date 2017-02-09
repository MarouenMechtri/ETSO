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


import requests
import time
import json
from bottle import request, response

config_file = open('plugins/config.json')
config_data = json.load(config_file)
ODL = config_data["ODL"]
ODL_PORT = config_data["ODL_PORT"]
ODL_USERNAME = config_data["ODL_USERNAME"]
ODL_PASSWORD = config_data["ODL_PASSWORD"]

SF_URL = "http://" + ODL + ":" + str(ODL_PORT) + "/restconf/config/service-function:service-functions/"
SFF_URL = "http://" + ODL + ":" + str(ODL_PORT) + "/restconf/config/service-function-forwarder:service-function-forwarders/"
SFC_URL = "http://" + ODL + ":" + str(ODL_PORT) + "/restconf/config/service-function-chain:service-function-chains/"
SFP_URL = "http://" + ODL + ":" + str(ODL_PORT) + "/restconf/config/service-function-path:service-function-paths/"
RSP_RPC_URL = "http://" + ODL + ":" + str(ODL_PORT) + "/restconf/operations/rendered-service-path:create-rendered-path"



def odl_create_vnfs(body):
    s = requests.Session()
    print("POSTing {} \n".format(SF_URL))
    r = s.put(SF_URL, data=body, headers={'content-type': 'application/json'},
              stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
    if r.status_code in {200,201}:
        print("Checking... \n")
        # Creation of SFs is slow, need to pause here.
        time.sleep(2)
        r = s.get(SF_URL, stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
        if (r.status_code in {200,201}):
            print("=>Creation successfully, status code: {} \n".format(r.status_code))
            response.status = r.status_code
    else:
        print("=>Failure, status code: {} \n".format(r.status_code))
        response.status = r.status_code
    return r.status_code




def odl_create_cps(body):
    s = requests.Session()
    print("POSTing {} \n".format(SFF_URL))
    r = s.put(SFF_URL, data=body, headers={'content-type': 'application/json'},
              stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
    if r.status_code in {200,201}:
        print("Checking... \n")
        # Creation of SFFs is slow, need to pause here.
        time.sleep(2)
        r = s.get(SFF_URL, stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
        if (r.status_code in {200,201}):
            print("=>Creation successfully, status code: {} \n".format(r.status_code))
            response.status = r.status_code
    else:
        print("=>Failure, status code: {} \n".format(r.status_code))
        response.status = r.status_code
    return r.status_code



def odl_create_vnf_fg(body):
    s = requests.Session()
    print("POSTing {} \n".format(SFC_URL))
    r = s.put(SFC_URL, data=body, headers={'content-type': 'application/json'},
              stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
    if r.status_code in {200,201}:
        print("Checking... \n")
        # Creation of SFCs is slow, need to pause here.
        time.sleep(2)
        r = s.get(SFC_URL, stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
        if (r.status_code in {200,201}):
            print("=>Creation successfully, status code: {} \n".format(r.status_code))
            response.status = r.status_code
    else:
        print("=>Failure, status code: {} \n".format(r.status_code))
        response.status = r.status_code
    return r.status_code



def odl_create_fps(body):
    s = requests.Session()
    print("POSTing {} \n".format(SFP_URL))
    r = s.put(SFP_URL, data=body, headers={'content-type': 'application/json'},
              stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
    if r.status_code in {200,201}:
        print("Checking... \n")
        # Creation of SFPs is slow, need to pause here.
        time.sleep(2)
        r = s.get(SFP_URL, stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
        if (r.status_code in {200,201}):
            print("=>Creation successfully, status code: {} \n".format(r.status_code))
            response.status = r.status_code
    else:
        print("=>Failure, status code: {} \n".format(r.status_code))
        response.status = r.status_code
    return r.status_code


def odl_create_rfps(body):
    s = requests.Session()
    print("POSTing RPC {} \n".format(RSP_RPC_URL))
    r = s.post(RSP_RPC_URL, data=body, headers={'content-type': 'application/json'},
               stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
    if r.status_code in {200,201}:
        print("Checking... \n")
        time.sleep(2)
        print("=>Creation successfully, status code: {} \n".format(r.status_code))
        response.status = r.status_code
    else:
        print("=>Failure, status code: {} \n".format(r.status_code))
        response.status = r.status_code
    return r.status_code


def odl_delete_vnfs():
    s = requests.Session()
    r = s.delete(SF_URL, stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
    if r.status_code in {200,201}:
        print("=>Deleted all Service Functions \n")
        response.status = r.status_code
    else:
        print("=>Failure to delete SFs, response code = {} \n".format(r.status_code))
        response.status = r.status_code
    return r.status_code

def odl_delete_vnf_fg():
    s = requests.Session()
    r = s.delete(SFC_URL, stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
    if r.status_code in {200,201}:
        print("=>Deleted all Service Function Chains \n")
        response.status = r.status_code
    else:
        print("=>Failure to delete SFCs, response code = {} \n".format(r.status_code))
        response.status = r.status_code
    return r.status_code

def odl_delete_cps():
    s = requests.Session()
    r = s.delete(SFF_URL, stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
    if r.status_code in {200,201}:
        print("=>Deleted all Service Function Forwarders \n")
        response.status = r.status_code
    else:
        print("=>Failure to delete SFFs, response code = {} \n".format(r.status_code))
        response.status = r.status_code
    return r.status_code

def odl_delete_fps():
    s = requests.Session()
    r = s.delete(SFP_URL, stream=False, auth=(ODL_USERNAME, ODL_PASSWORD))
    if r.status_code in {200,201}:
        print("=>Deleted all Service Function Paths \n")
        response.status = r.status_code
    else:
        print("=>Failure to delete SFPs, response code = {} \n".format(r.status_code))
        response.status = r.status_code
    return r.status_code

