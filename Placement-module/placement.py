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
Created on Feb 15, 2016
@authors: Marouen Mechtri, Chaima Ghribi
@contacts: {marouen.mechtri, chaima.ghribi}@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""


import bottle
import requests
import time
import json
import os
import re
import uuid
import yaml
import subprocess
from bottle import route, run, static_file, request, response


config_file = open('config.json')
config_data = json.load(config_file)
port = config_data["port"]
server = config_data["server"]
monitoring_server = config_data["monitoring_server"]
monitoring_port = config_data["monitoring_port"]

MONI_URL = "http://" + monitoring_server + ":" + str(monitoring_port) + "/infrastructure/reserved_resources"


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

@route('/placement', method='POST')
def placement():

    algo = bottle.request.get_header('algorithm')

    version = bottle.request.get_header('version')
    username = bottle.request.get_header('username')
    password = bottle.request.get_header('password')
    endpoint = bottle.request.get_header('endpoint')
    tenant_name = bottle.request.get_header('tenant_name')
    tenant_id = bottle.request.get_header('tenant_id')
    service = bottle.request.get_header('service')
    region = bottle.request.get_header('region')

    listVMs_json = json.loads(request._get_body_string())
    nbVMs = 0
    listVMs = {}

    for resource in listVMs_json:
        listVMs[listVMs_json[resource]['order']] = {}
        listVMs[listVMs_json[resource]['order']]['cpu'] = listVMs_json[resource]['num_cpus']
        listVMs[listVMs_json[resource]['order']]['mem'] = listVMs_json[resource]['mem_size']
        listVMs[listVMs_json[resource]['order']]['sto'] = listVMs_json[resource]['disk_size']
        listVMs[listVMs_json[resource]['order']]['name'] = resource
        nbVMs = nbVMs + 1




    instanceIG_file = open("instanceIG" + str(nbVMs) + "-0", "w")
    instanceIG_file.write("Number of Servers\n")
    instanceIG_file.write(str(nbVMs) + " 1 1\n")
    instanceIG_file.write("Nodes\n")
    for vm in listVMs:
        instanceIG_file.write(str(vm) + " " + str(vm) + " " + str(listVMs[vm]['cpu']) + " 3 1 0\n")

    instanceIG_file.write("EDGES\n")
    for i in range(nbVMs-1):
        instanceIG_file.write(str(i) + " " + str(i+1) + " 100\n")

    instanceIG_file.close()


    s = requests.Session()
    print("GETing {} \n".format(MONI_URL))
    headers = {}
    headers['content-type'] = 'application/json'
    headers['version'] = version
    headers['username'] = username
    headers['password'] = password
    headers['endpoint'] = endpoint
    headers['tenant_name'] = tenant_name
    headers['tenant_id'] = tenant_id
    headers['service'] = service
    headers['region'] = region

    r = s.get(MONI_URL, headers=headers, stream=False)
    if r.status_code == 200:
        servers=json.loads(r.text)
        sorted_servers = sorted(servers['Reserved_resources']['CPU']['CPU_free_size'], key=natural_keys)
        instanceRG_file = open("instanceRG" + str(len(sorted_servers)) + "-0", "w")
        instanceRG_file.write("Number of Nodes, Number of Servers\n")
        instanceRG_file.write(str(len(sorted_servers)) + " " + str(len(sorted_servers)) + "\n")
        instanceRG_file.write("Nodes\n")
        index_server = 0
        for server in sorted_servers:
            instanceRG_file.write(str(index_server) + " S:" + str(index_server) + " " +
                                  str(servers['Reserved_resources']['CPU']['CPU_free_size'][server]) + " 0\n")
            index_server = index_server + 1

        instanceRG_file.write("EDGES\n")
        for i in range(len(sorted_servers) - 1):
            for j in range(len(sorted_servers) - 1, i, -1):
                instanceRG_file.write(str(i) + " " + str(j) + " 1000\n")

        instanceRG_file.close()


    else:
        print("=>Failure, status code: {} \n".format(r.status_code))
        response.status = r.status_code


    subprocess.call(['java', '-jar', 'placementAlgo.jar', 'nbNodeRG='+str(len(sorted_servers)), 'nbServerIG='+str(nbVMs), 'indexRG=0', 'indexIG=0',  algo + '=true'])

    if algo=='mcts':
        SolutionMapping_file_name = "SolutionMappingMCTS-instanceRG" + str(len(sorted_servers)) + "-0-instanceIG" + str(
            nbVMs) + "-0"
    if algo == 'greedy':
        SolutionMapping_file_name = "SolutionMappingGreedy-instanceRG" + str(len(sorted_servers)) + "-0-instanceIG" + str(
            nbVMs) + "-0"
    if algo == 'eigen':
        SolutionMapping_file_name = "SolutionMappingEigen-instanceRG" + str(len(sorted_servers)) + "-0-instanceIG" + str(
            nbVMs) + "-0"

    SolutionMapping_file = open(SolutionMapping_file_name, "r")
    mapping_solution = {}
    for j in range(nbVMs):
        line = SolutionMapping_file.readline()
        mapping_solution[listVMs[int(line.split()[0])]['name']] = sorted_servers[int(line.split()[1])]

    return mapping_solution



run(host=server, port=port, debug=True)
