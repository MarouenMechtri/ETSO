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
TARGET_CLASS_NAME = 'ToscaCP'


class ToscaCP(HotResource):
    '''Translate TOSCA node type tosca.nodes.nfv.CP.'''

    toscatype = 'tosca.nodes.nfv.CP'

    def __init__(self, nodetemplate):
        super(ToscaCP, self).__init__(nodetemplate,
                                      type='tosca.nodes.nfv.CP')
        pass

    def handle_properties(self):
        #print self.__dict__
        self.properties['name'] = self.nodetemplate.name
        self.properties['ip-mgmt-address'] = self.nodetemplate.templates[self.nodetemplate.name]['attributes']['IP_address']
        if (self.nodetemplate.templates[self.nodetemplate.name]['attributes']['IP_address']):
            self.properties['rest-uri'] = 'http://' + str(self.nodetemplate.templates[self.nodetemplate.name]['attributes']['IP_address']) + ':5000'
        else:
            self.properties['rest-uri'] = self.nodetemplate.templates[self.nodetemplate.name]['attributes']['IP_address']

        for vl in self.depends_on:
            if (vl.type == 'tosca.nodes.nfv.VL'):
                self.properties['sff-data-plane-locator'] = []
                sff_data_plane_locator = {}
                sff_data_plane_locator['name'] = \
                    self.nodetemplate.templates[self.nodetemplate.name]['attributes']['interface']
                sff_data_plane_locator['data-plane-locator'] = {}
                sff_data_plane_locator['data-plane-locator']['transport'] \
                    = "service-locator:" + str(vl.nodetemplate.templates[vl.nodetemplate.name]['attributes']['transport_type'])
                sff_data_plane_locator['data-plane-locator']['ip'] \
                    = self.nodetemplate.templates[self.nodetemplate.name]['attributes']['IP_address']
                sff_data_plane_locator['data-plane-locator']['port']  = \
                    self.nodetemplate.templates[self.nodetemplate.name]['attributes']['port']
                self.properties['sff-data-plane-locator'].append(sff_data_plane_locator)

                self.properties['service-function-dictionary'] = []
                service_function_dictionary = {}
                service_function_dictionary['sff-sf-data-plane-locator'] = {}
		#### For SFC-ODL Lithium ####
                #service_function_dictionary['sff-sf-data-plane-locator']['transport'] \
                #    = "service-locator:" + str(vl.nodetemplate.templates[vl.nodetemplate.name]['attributes']['transport_type'])

                for requirement in self.nodetemplate.requirements:
                    if 'virtualBinding' in requirement.keys():
                        service_function_dictionary['name'] = requirement['virtualBinding']
			#### For SFC-ODL Lithium ####
                        #service_function_dictionary['type'] = \
                        #    "service-function-type:" + self.nodetemplate.templates[requirement['virtualBinding']]['attributes']['type']
                        #service_function_dictionary['sff-sf-data-plane-locator']['ip'] \
                        #    = self.nodetemplate.templates[requirement['virtualBinding']]['attributes']['address']
                        #service_function_dictionary['sff-sf-data-plane-locator']['port']  = \
                        #    self.nodetemplate.templates[requirement['virtualBinding']]['attributes']['port']
                        self.properties['service-node'] = \
                            self.nodetemplate.templates[requirement['virtualBinding']]['requirements'][0]['host']
                self.properties['service-function-dictionary'].append(service_function_dictionary)


