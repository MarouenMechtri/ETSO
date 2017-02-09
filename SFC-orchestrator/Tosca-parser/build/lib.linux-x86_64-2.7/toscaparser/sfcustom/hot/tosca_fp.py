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
TARGET_CLASS_NAME = 'ToscaFP'


class ToscaFP(HotResource):
    '''Translate TOSCA node type tosca.nodes.nfv.FP.'''

    toscatype = 'tosca.nodes.nfv.FP'

    def __init__(self, nodetemplate):
        super(ToscaFP, self).__init__(nodetemplate,
                                      type='tosca.nodes.nfv.FP')
        pass


    def handle_properties(self):
        self.properties['name'] = self.nodetemplate.name
        self.properties['sfc-service-function']=[]
        i = 0

        for cp in self.depends_on:
            vnf = {}
            for requirement in self.nodetemplate.templates[cp.name]['requirements']:
                if ('virtualBinding' in requirement.keys()):
                    vnf['type']= 'service-function-type:' + str(self.nodetemplate.templates[requirement.values()[0]]['attributes']['type'])
                    vnf['name']= str(self.nodetemplate.templates[requirement.values()[0]]['attributes']['type']) + '-abstract'
            vnf['order']= i
            i = i + 1
            self.properties['sfc-service-function'].append(vnf)


