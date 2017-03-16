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

import os
import sys
import uuid
import requests
import yaml
import credentials
import bottle
from bottle import route, run, static_file, request, response

from novaclient import client
import novaclient
from packaging import version as pack_version

from toscaparser.tosca_template import ToscaTemplate
from toscaparser.sfc.tosca_translator import TOSCATranslator
from toscaparser.utils.gettextutils import _
from toscaparser.utils.urlutils import UrlUtils
from RequestManager.decomposer import *


config_file = open('config.json')
config_data = json.load(config_file)
port = config_data["port"]
server = config_data["server"]

placement_server = config_data["placement_server"]
placement_port = config_data["placement_port"]
PLACEMENT_URL = "http://" + placement_server + ":" + str(placement_port) + "/placement"


nctManager_server = config_data["nctManager_server"]
nctManager_port = config_data["nctManager_port"]
NCT_Manager_stack_create_URL = "http://" + nctManager_server + ":" + str(nctManager_port) + "/stack_create"
NCT_Manager_stack_output_URL = "http://" + nctManager_server + ":" + str(nctManager_port) + "/stack_output"
NCT_Manager_stack_delete_URL = "http://" + nctManager_server + ":" + str(nctManager_port) + "/stack_delete"

sfcManager_server = config_data["sfcManager_server"]
sfcManager_port = config_data["sfcManager_port"]
VNF_URL = "http://" + sfcManager_server + ":" + str(sfcManager_port) + "/vnfs"
CP_URL = "http://" + sfcManager_server + ":" + str(sfcManager_port) + "/cps"
VNF_FG_URL = "http://" + sfcManager_server + ":" + str(sfcManager_port) + "/vnf-fg"
FP_URL = "http://" + sfcManager_server + ":" + str(sfcManager_port) + "/fps"
RFP_URL = "http://" + sfcManager_server + ":" + str(sfcManager_port) + "/rfps"


def main():
    if len(sys.argv) < 3:
        msg = _("The program requires minimum two arguments. "
                "Please refer to the usage documentation.")
        raise ValueError(msg)
    if "--template-file=" not in sys.argv[1]:
        msg = _("The program expects --template-file as first argument. "
                "Please refer to the usage documentation.")
        raise ValueError(msg)
    if "--template-type=" not in sys.argv[2]:
        msg = _("The program expects --template-type as second argument. "
                "Please refer to the usage documentation.")
        raise ValueError(msg)
    path = sys.argv[1].split('--template-file=')[1]
    # e.g. --template_file=translator/tests/data/tosca_helloworld.yaml
    template_type = sys.argv[2].split('--template-type=')[1]
    # e.g. --template_type=tosca
    supported_types = ['tosca']
    if not template_type:
        raise ValueError(_("Template type is needed. For example, 'tosca'"))
    elif template_type not in supported_types:
        raise ValueError(_("%(value)s is not a valid template type.")
                         % {'value': template_type})
    parsed_params = {}
    if len(sys.argv) > 3:
        parsed_params = parse_parameters(sys.argv[3])

    a_file = os.path.isfile(path)
    a_url = UrlUtils.validate_url(path) if not a_file else False
    if a_file or a_url:
        heat_tpl = orchetration(path, parsed_params, a_file)
        #if heat_tpl:
        #    write_output(heat_tpl)
    else:
        raise ValueError(_("The path %(path)s is not a valid file or URL.") %
                         {'path': path})


def parse_parameters(parameter_list):
    parsed_inputs = {}
    if parameter_list.startswith('--parameters'):
        inputs = parameter_list.split('--parameters=')[1].\
            replace('"', '').split(';')
        for param in inputs:
            keyvalue = param.split('=')
            parsed_inputs[keyvalue[0]] = keyvalue[1]
    else:
        raise ValueError(_("%(param) is not a valid parameter.")
                         % parameter_list)
    return parsed_inputs

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the randomregionOne string.


def MappingZoneHost():
    username = credentials.USERNAME
    password = credentials.PASSWORD
    tenant_name = credentials.TENANT_NAME
    tenant_id = credentials.TENANT_ID
    endpoint = credentials.ENDPOINT
    service = credentials.SERVICE
    region = credentials.REGION
    version = credentials.VERSION
    if pack_version.parse(novaclient.__version__) < pack_version.parse("7.0.0"):
        nova_client = client.Client(version, username, password,
                                tenant_name, endpoint,
                                service_type=service,
                                region_name=region)
    else:
        nova_client = client.Client(version, username, password,
                                    tenant_id, endpoint,
                                    service_type=service,
                                    region_name=region)
    host_to_zone = {}
    for zone in nova_client.availability_zones.list():

        for host in zone.hosts:
            host_to_zone[host] = zone.zoneName


    return host_to_zone


@route('/deploy_template', method='POST')
def deploy_template():


    stack_name = my_random_string()

    request_file = open('requests/'+stack_name+'.yaml','w')
    request_file.write(request._get_body_string())
    request_file.close()

    orchetration('requests/'+stack_name+'.yaml', {}, True, stack_name)

    return stack_name



@route('/delete_template', method='DELETE')
def delete_template():
    uuid = bottle.request.get_header('uuid')

    headers = {}
    headers['content-type'] = 'application/json'
    headers['version'] = str(credentials.VERSION)
    headers['username'] = credentials.USERNAME
    headers['password'] = credentials.PASSWORD
    headers['endpoint'] = credentials.ENDPOINT
    headers['tenant_name'] = credentials.TENANT_NAME
    headers['tenant_id'] = credentials.TENANT_ID
    headers['service'] = credentials.SERVICE
    headers['region'] = credentials.REGION
    headers['heat_url'] = credentials.HEAT_URL
    headers['uuid'] = uuid
    s = requests.Session()
    r = s.delete(NCT_Manager_stack_delete_URL, headers=headers, stream=False)
    print r.text





def orchetration(path, parsed_params, a_file, stack_name):



    tosca = ToscaTemplate(path, parsed_params, a_file)
    translator = TOSCATranslator(tosca, parsed_params)
    translator.translate()

    decomposed_request = request_decomposition(tosca, translator, stack_name, False)

    '''Calling Placement Module'''

    s = requests.Session()
    print("[POSTing] from the orchestrator to the placement module: {} \n".format(PLACEMENT_URL))
    placement_headers = {}
    placement_headers['content-type'] = 'application/json'
    placement_headers['algorithm'] = 'greedy'
    placement_headers['version'] = str(credentials.VERSION)
    placement_headers['username'] = credentials.USERNAME
    placement_headers['password'] = credentials.PASSWORD
    placement_headers['endpoint'] = credentials.ENDPOINT
    placement_headers['tenant_name'] = credentials.TENANT_NAME
    placement_headers['tenant_id'] = credentials.TENANT_ID
    placement_headers['service'] = credentials.SERVICE
    placement_headers['region'] = credentials.REGION

    r = s.post(PLACEMENT_URL, data=decomposed_request['request'], headers=placement_headers, stream=False)

    '''Calling Request Manager to update NCT template'''

    if r.status_code == 200:
        zone_to_host = MappingZoneHost()
        location = {}
        for key, value in json.loads(r.text).iteritems():
            location[key] = str(zone_to_host[value])
        decomposed_request['nct'] = add_vm_location(translator, location)
        decomposed_request['nct'] = add_odl_address(translator, location)

    '''Calling NCT Manager to instantiate NCT template'''

    s = requests.Session()
    print("[POSTing] from the orchestrator to the NCT Manager module: {} \n".format(NCT_Manager_stack_create_URL))
    headers = {}
    headers['content-type'] = 'application/json'
    headers['version'] = str(credentials.VERSION)
    headers['username'] = credentials.USERNAME
    headers['password'] = credentials.PASSWORD
    headers['endpoint'] = credentials.ENDPOINT
    headers['tenant_name'] = credentials.TENANT_NAME
    headers['tenant_id'] = credentials.TENANT_ID
    headers['service'] = credentials.SERVICE
    headers['region'] = credentials.REGION
    headers['heat_url'] = credentials.HEAT_URL
    headers['stack_name'] = 'nct_' + stack_name
    r = s.post(NCT_Manager_stack_create_URL, data=decomposed_request['nct'], headers=headers, stream=False)
    if r.status_code == 200:
        uuid = r.text

    '''Calling NCT Manager to get NCT template output'''

    # uuid = 'cc4d6e33-d0aa-4fbd-9322-97d61f757a9f'

    s = requests.Session()
    print("[GETing] from the orchestrator to the NCT Manager module: {} \n".format(NCT_Manager_stack_output_URL))
    headers['uuid'] = uuid
    r = s.get(NCT_Manager_stack_output_URL, data=decomposed_request['output'], headers=headers, stream=False)

    '''Calling Request Manager to update sf and sff templates'''

    if r.status_code == 200:
        sf_sff_template = update_sf_sff_templates(decomposed_request['sf'], decomposed_request['sff'], r.text)
        decomposed_request['sf'] = sf_sff_template['sf']
        decomposed_request['sff'] = sf_sff_template['sff']

        '''Calling SFC Manager to instantiate VNFs resources'''

        s = requests.Session()
        print("[POSTing] from the orchestrator to the SFC Manager module: {} \n".format(VNF_URL))
        r = s.post(VNF_URL, data=json.dumps(decomposed_request['sf']), headers={'content-type': 'application/json'},
                   stream=False)
        if r.status_code in {200,201}:
            print("====>VNF Creation successfully")
        else:
            print("====>VNF Failure, status code: {} \n".format(r.status_code))

        '''Calling SFC Manager to instantiate CPs resources'''

        print("[POSTing] from the orchestrator to the SFC Manager module: {} \n".format(CP_URL))
        r = s.post(CP_URL, data=json.dumps(decomposed_request['sff']), headers={'content-type': 'application/json'},
                   stream=False)
        if r.status_code in {200,201}:
            print("====>CP Creation successfully")
        else:
            print("====>CP Failure, status code: {} \n".format(r.status_code))

        '''Calling SFC Manager to instantiate SFC resources'''

        print("[POSTing] from the orchestrator to the SFC Manager module: {} \n".format(VNF_FG_URL))
        r = s.post(VNF_FG_URL, data=json.dumps(decomposed_request['sfc']), headers={'content-type': 'application/json'},
                   stream=False)
        if r.status_code in {200,201}:
            print("====>VNF-FG Creation successfully")
        else:
            print("====>VNF-FG Failure, status code: {} \n".format(r.status_code))

        '''Calling SFC Manager to instantiate SFPs resources'''

        print("[POSTing] from the orchestrator to the SFC Manager module: {} \n".format(FP_URL))
        r = s.post(FP_URL, data=json.dumps(decomposed_request['sfp']), headers={'content-type': 'application/json'},
                   stream=False)
        if r.status_code in {200,201}:
            print("====>FP Creation successfully")
        else:
            print("====>FP Failure, status code: {} \n".format(r.status_code))

        '''Calling SFC Manager to instantiate RSPs resources'''
        print("[POSTing] from the orchestrator to the SFC Manager module: {} \n".format(RFP_URL))
        r = s.post(RFP_URL, data=json.dumps(decomposed_request['rsp']), headers={'content-type': 'application/json'},
                   stream=False)
        if r.status_code in {200,201}:
            print("====>RFP Creation successfully")
        else:
            print("====>RFP Failure, status code: {} \n".format(r.status_code))

run(host=server, port=port, debug=True)

#if __name__ == '__main__':
#   main()