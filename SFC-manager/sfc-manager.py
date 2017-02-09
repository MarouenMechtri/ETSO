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


from bottle import route, run, static_file, request, response
from plugins.ODL_plugin import *
from plugins.ONOS_plugin import *


config_file = open('config.json')
config_data = json.load(config_file)
port = config_data["port"]
server = config_data["server"]
plugin = config_data["plugin"]



@route('/vnfs', method='POST')
def create_vnfs():
    if plugin == "odl":
        print odl_create_vnfs(json.loads(request._get_body_string()))
    if plugin == "onos":
        print onos_create_vnfs(request._get_body_string())



@route('/cps', method='POST')
def create_cps():
    if plugin == "odl":
        print odl_create_cps(json.loads(request._get_body_string()))
    if plugin == "onos":
        print onos_create_cps(request._get_body_string())


@route('/vnf-fg', method='POST')
def create_vnf_fg():
    if plugin == "odl":
        print odl_create_vnf_fg(json.loads(request._get_body_string()))
    if plugin == "onos":
        print onos_create_vnf_fg(request._get_body_string())


@route('/fps', method='POST')
def create_fps():
    if plugin == "odl":
        print odl_create_fps(json.loads(request._get_body_string()))
    if plugin == "onos":
        print onos_create_fps(request._get_body_string())


@route('/rfps', method='POST')
def create_rfps():
    if plugin == "odl":
        print odl_create_rfps(json.loads(request._get_body_string()))
    if plugin == "onos":
        print onos_create_rfps(request._get_body_string())



@route('/vnfs', method='DELETE')
def delete_vnfs():
    if plugin == "odl":
        odl_delete_vnfs()
    if plugin == "onos":
        onos_delete_vnfs()


@route('/vnf-fg', method='DELETE')
def delete_vnf_fg():
    if plugin == "odl":
        odl_delete_vnf_fg()
    if plugin == "onos":
        onos_delete_vnf_fg()

@route('/cps', method='DELETE')
def delete_cps():
    if plugin == "odl":
        odl_delete_cps()
    if plugin == "onos":
        onos_delete_cps()

@route('/fps', method='DELETE')
def delete_fps():
    if plugin == "odl":
        odl_delete_fps()
    if plugin == "onos":
        onos_delete_fps()


@route('/clean', method='DELETE')
def delete_vnfs():
    if plugin == "odl":
        odl_delete_cps()
        odl_delete_vnfs()
        odl_delete_fps()
        odl_delete_vnf_fg()
    if plugin == "onos":
        onos_delete_cps()
        onos_delete_vnfs()
        onos_delete_fps()
        onos_delete_vnf_fg()


run(host=server, port=port, debug=True)
