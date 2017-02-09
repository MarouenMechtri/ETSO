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

from translator.hot.syntax.hot_resource import HotResource

# Name used to dynamically load appropriate map class.
TARGET_CLASS_NAME = 'ToscaVNF'


class ToscaVNF(HotResource):
    '''Translate TOSCA node type tosca.nodes.nfv.VNF.'''

    toscatype = 'tosca.nodes.nfv.VNF'

    def __init__(self, nodetemplate):
        super(ToscaVNF, self).__init__(nodetemplate,
                                      type='tosca.nodes.nfv.VNF')
        pass

    def handle_properties(self):
        self.properties['name'] = self.nodetemplate.name
        self.properties['ip-mgmt-address'] = self.nodetemplate.templates[self.nodetemplate.name]['attributes']['address']
        if (self.nodetemplate.templates[self.nodetemplate.name]['attributes']['address']):
            self.properties['rest-uri'] = 'http://' + str(self.nodetemplate.templates[self.nodetemplate.name]['attributes']['address']) + ':5000'
        else:
            self.properties['rest-uri'] = self.nodetemplate.templates[self.nodetemplate.name]['attributes']['address']
        self.properties['nsh-aware'] = self.nodetemplate.templates[self.nodetemplate.name]['attributes']['nsh_aware']
        self.properties['type'] = 'service-function-type:' + str(self.nodetemplate.templates[self.nodetemplate.name]['attributes']['type'])
        self.properties['sf-data-plane-locator'] = []


        for node in self.nodetemplate.templates:
            if (self.nodetemplate.templates[node]['type'] == 'tosca.nodes.nfv.CP'):
                for requirement in self.nodetemplate.templates[node]['requirements']:

                    if ('virtualBinding' in requirement.keys()) and  (self.nodetemplate.name in requirement.values()):

                        sf_data_plane_locator = {}
                        sf_data_plane_locator['service-function-forwarder'] = node
                        sf_data_plane_locator['ip'] = self.nodetemplate.templates[self.nodetemplate.name]['attributes']['address']
                        sf_data_plane_locator['name'] = 'vxlan'

                        sf_data_plane_locator['port'] = self.nodetemplate.templates[self.nodetemplate.name]['attributes']['port']

                        for virtuallink_req in self.nodetemplate.templates[node]['requirements']:
                            if ('virtualLink' in virtuallink_req.keys()):
                                sf_data_plane_locator['transport'] =  \
                                    'service-locator:' + str(self.nodetemplate.templates[virtuallink_req.values()[0]]['attributes']['transport_type'])
                        self.properties['sf-data-plane-locator'].append(sf_data_plane_locator)

