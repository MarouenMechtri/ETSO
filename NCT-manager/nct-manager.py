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
import os
import uuid
import bottle
from bottle import route, run, static_file, request, response
from plugins.heat_plugin import *
from plugins.cloudify_plugin import *

config_file = open('config.json')
config_data = json.load(config_file)
port = config_data["port"]
server = config_data["server"]
plugin = config_data["plugin"]


@route('/stack_create', method='POST')
def create_stack():

    if plugin == "heat":

        version = bottle.request.get_header('version')
        username = bottle.request.get_header('username')
        password = bottle.request.get_header('password')
        endpoint = bottle.request.get_header('endpoint')
        tenant_name = bottle.request.get_header('tenant_name')
        tenant_id = bottle.request.get_header('tenant_id')
        service = bottle.request.get_header('service')
        region = bottle.request.get_header('region')
        heat_url = bottle.request.get_header('heat_url')
        stack_name = bottle.request.get_header('stack_name')

        stack = stack_create_heat(username, password, endpoint, tenant_name, heat_url, request._get_body_string(), stack_name)
        return stack['stack']['id']
    if plugin == "cloudify":
       stack_create_cloudify(request._get_body_string())



@route('/stack_delete', method='DELETE')
def delete_stack():
    if plugin == "heat":

        version = bottle.request.get_header('version')
        username = bottle.request.get_header('username')
        password = bottle.request.get_header('password')
        endpoint = bottle.request.get_header('endpoint')
        tenant_name = bottle.request.get_header('tenant_name')
        tenant_id = bottle.request.get_header('tenant_id')
        service = bottle.request.get_header('service')
        region = bottle.request.get_header('region')
        heat_url = bottle.request.get_header('heat_url')

        stack_uuid = bottle.request.get_header('uuid')
        stack_delete_heat(username, password, endpoint, tenant_name, heat_url, stack_uuid)
    if plugin == "cloudify":
        stack_uuid = bottle.request.get_header('uuid')
        stack_delete_cloudify(stack_uuid)



@route('/stack_status', method='GET')
def status_stack():

    if plugin == "heat":

        version = bottle.request.get_header('version')
        username = bottle.request.get_header('username')
        password = bottle.request.get_header('password')
        endpoint = bottle.request.get_header('endpoint')
        tenant_name = bottle.request.get_header('tenant_name')
        tenant_id = bottle.request.get_header('tenant_id')
        service = bottle.request.get_header('service')
        region = bottle.request.get_header('region')
        heat_url = bottle.request.get_header('heat_url')

        stack_uuid = bottle.request.get_header('uuid')
        return stack_status_heat(username, password, endpoint, tenant_name, heat_url, stack_uuid)
    if plugin == "cloudify":
        stack_uuid = bottle.request.get_header('uuid')
        return stack_status_cloudify(stack_uuid)

@route('/stack_output', method='GET')
def output_stack():

    if plugin == "heat":

        version = bottle.request.get_header('version')
        username = bottle.request.get_header('username')
        password = bottle.request.get_header('password')
        endpoint = bottle.request.get_header('endpoint')
        tenant_name = bottle.request.get_header('tenant_name')
        tenant_id = bottle.request.get_header('tenant_id')
        service = bottle.request.get_header('service')
        region = bottle.request.get_header('region')
        heat_url = bottle.request.get_header('heat_url')

        stack_uuid = bottle.request.get_header('uuid')
        stack_data = stack_output_heat(username, password, endpoint, tenant_name, heat_url, stack_uuid, request._get_body_string())
        return stack_data
    if plugin == "cloudify":
       stack_output_cloudify(request._get_body_string())


run(host=server, port=port, debug=True)