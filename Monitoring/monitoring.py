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

import json
import bottle
from bottle import route, run, static_file, request, response, Bottle,redirect,template

import compute_node
import infrastructure

config_file = open('config.json')
config_data = json.load(config_file)
port = config_data["port"]
server = config_data["server"]


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()



@route('/infrastructure_state', method='GET')
def infra_data():

    run_vm={}
    num_vm={}

    version = bottle.request.get_header('version')
    username = bottle.request.get_header('username')
    password = bottle.request.get_header('password')
    endpoint = bottle.request.get_header('endpoint')
    tenant_name = bottle.request.get_header('tenant_name')
    tenant_id = bottle.request.get_header('tenant_id')
    service = bottle.request.get_header('service')
    region = bottle.request.get_header('region')


    #version = credentials.VERSION
    #username = credentials.USERNAME
    #password = credentials.PASSWORD
    #tenant = credentials.TENANT
    #endpoint = credentials.ENDPOINT
    #service = credentials.SERVICE
    #region = credentials.REGION


    infra=infrastructure.Infrastructure(version, username, password, tenant_name, tenant_id, endpoint, service, region)
    compute=compute_node.Compute_node(infra)
    ip_list={}
    for compute_name in infra.get_compute_nodes_name_list():
        ip_add=compute.get_ip_add(compute_name)
        ip_list[compute_name]=ip_add
        list_vm=compute.get_name_of_VMs_of_compute_node(compute_name)
        run_vm[compute_name]=list_vm
        num_runn_vms=compute.get_name_of_VMs_of_compute_node(compute_name).__len__()
        num_vm[compute_name]=num_runn_vms
    number_compute_nodes=infra.get_number_compute_nodes()
    idle_compute=infra.get_list_of_idle_compute_nodes()
    num_idle_compute_nodes=infra.get_number_of_idle_compute_nodes()
    percentage_idle_compute_nodes=infra.get_percentage_used_compute_nodes()
    return {"success": True, "Infrastructure ":{"Compute_nodes":ip_list,"Number of compute nodes": number_compute_nodes,"IDLE compute nodes":idle_compute,"Number of idle compute nodes":num_idle_compute_nodes,"Percentage of used compute nodes": percentage_idle_compute_nodes,"List_of_running_vms":run_vm,"Number of running VMs":num_vm}}


@route('/infrastructure/reserved_resources', method='GET')
def reserved_metrics():
    cpu_tot={}
    cpu_free={}
    disk_tot={}
    disk_free={}
    memory_tot={}
    memory_free={}

    version = bottle.request.get_header('version')
    username = bottle.request.get_header('username')
    password = bottle.request.get_header('password')
    endpoint = bottle.request.get_header('endpoint')
    tenant_name = bottle.request.get_header('tenant_name')
    tenant_id = bottle.request.get_header('tenant_id')
    service = bottle.request.get_header('service')
    region = bottle.request.get_header('region')

    #version = credentials.VERSION
    #username = credentials.USERNAME
    #password = credentials.PASSWORD
    #tenant = credentials.TENANT
    #endpoint = credentials.ENDPOINT
    #service = credentials.SERVICE
    #region = credentials.REGION

    infra=infrastructure.Infrastructure(version, username, password, tenant_name, tenant_id, endpoint, service, region)
    compute=compute_node.Compute_node(infra)
    for compute_name in infra.get_compute_nodes_name_list():
        total_CPU=compute.get_total_CPU(compute_name)
        cpu_tot[compute_name]=total_CPU
        free_cpu=compute.get_free_CPU_hyp(compute_name)
        cpu_free[compute_name]=free_cpu
        total_disk=compute.get_total_res_disk_size(compute_name)
        disk_tot[compute_name]=total_disk
        free_disk=compute.get_free_res_disk(compute_name)
        disk_free[compute_name]=free_disk
        total_mem=compute.get_total_memory_size(compute_name)
        memory_tot[compute_name]=total_mem
        free_mem=compute.get_free_res_memory(compute_name)
        memory_free[compute_name]=free_mem
    return {"success": True, "Reserved_resources":{"CPU":{"CPU_total_size":cpu_tot, "CPU_free_size":cpu_free},
                                                   "Disk":{"Disk_total_size (GB)":disk_tot,
                                                           "Disk_free_size (GB)": disk_free},
                                                   "Memory":{"Memory_total_size (MB)": memory_tot,
                                                             "Memory_free_size (MB)":memory_free}}}



if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--host", dest='host', default=server,
                      help="hostname or ip address", metavar="host")
    parser.add_option("--port", dest='port', default=port,
                      help="port number", metavar="port")
    (options, args) = parser.parse_args()
    run(host=server, port=port, debug=True)
