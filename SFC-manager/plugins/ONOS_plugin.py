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


def onos_create_vnfs(body):

    # TO be added
    return 200




def onos_create_cps(body):

    # TO be added
    return 200



def onos_create_vnf_fg(body):

    # TO be added
    return 200



def onos_create_fps(body):

    # TO be added
    return 200


def onos_create_rfps(body):

    # TO be added
    return 200


def onos_delete_vnfs():

    # TO be added
    return 200


def onos_delete_vnf_fg():

    # TO be added
    return 200



def onos_delete_cps():

    # TO be added
    return 200



def onos_delete_fps():

    # TO be added
    return 200

