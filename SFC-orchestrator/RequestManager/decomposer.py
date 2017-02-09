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



from toscaparser.sfc.syntax.hot_template import HotTemplate

def add_odl_address(translator, location):
    sfc_resources = ['tosca.nodes.nfv.CP', 'tosca.nodes.nfv.VL', 'tosca.nodes.nfv.VNF', 'tosca.nodes.nfv.FP',
                     'tosca.nodes.nfv.VNFFG']

    nct_template = HotTemplate()
    nct_template.description = translator.hot_template.description
    nct_template.parameters = translator.hot_template.parameters
    nct_template.outputs = translator.hot_template.outputs
    nct_template.resources = []
    for resource in translator.hot_template.resources:

        if resource.type not in sfc_resources:

            if resource.name in location:
                resource.properties['availability_zone'] = location[resource.name]
                resource.properties['user_data'] = {}
                resource.properties['user_data']['str_replace'] = {}
                script = "| \n " \
                         "#!/bin/bash \n " \
                         "/home/ubuntu/start_agent.sh $ODL > /tmp/sfc.log 2>&1 &"

                resource.properties['user_data']['str_replace']['template'] = script
                resource.properties['user_data']['str_replace']['params'] = {}
                resource.properties['user_data']['str_replace']['params']['$ODL'] = {}
                resource.properties['user_data']['str_replace']['params']['$ODL']['get_param'] = 'odl'



            nct_template.resources.append(resource)
            nct = nct_template.output_to_yaml()
            nct = nct.replace('\\n', '\n            ')
            nct = nct.replace('\"', '')
            nct = nct.replace('\\', ' ')
            nct = nct.replace('\n            --rest', ' --rest')

            #print nct

    return nct



def add_vm_location(translator, location):
    sfc_resources = ['tosca.nodes.nfv.CP', 'tosca.nodes.nfv.VL', 'tosca.nodes.nfv.VNF', 'tosca.nodes.nfv.FP',
                     'tosca.nodes.nfv.VNFFG']

    nct_template = HotTemplate()
    nct_template.description = translator.hot_template.description
    nct_template.parameters = translator.hot_template.parameters
    nct_template.outputs = translator.hot_template.outputs
    nct_template.resources = []
    for resource in translator.hot_template.resources:

        if resource.type not in sfc_resources:

            if resource.name in location:
                resource.properties['availability_zone'] = location[resource.name]

            nct_template.resources.append(resource)

    return nct_template.output_to_yaml()

def update_sf_sff_templates(sfs, sffs, new_data):
    sff_dict = json.loads(sffs)
    sf_dict = json.loads(sfs)
    new_data = json.loads(new_data)

    index_sff=0
    for sff in sff_dict['service-function-forwarders']['service-function-forwarder']:
        index_sf=0
        for sf in sf_dict['service-functions']['service-function']:
            if sf['name'] == sff['service-function-dictionary'][0]['name']:
                sf_dict['service-functions']['service-function'][index_sf]['ip-mgmt-address'] = new_data[sff['service-node']]['first_address']
                for i in range(0, len(sf_dict['service-functions']['service-function'][index_sf]['sf-data-plane-locator'])):
                    sf_dict['service-functions']['service-function'][index_sf]['sf-data-plane-locator'][i]['ip'] = new_data[sff['service-node']]['first_address']
                if sf_dict['service-functions']['service-function'][index_sf]['rest-uri']:
                    start = sf_dict['service-functions']['service-function'][index_sf]['rest-uri'].find('http://') + 7
                    end = sf_dict['service-functions']['service-function'][index_sf]['rest-uri'].find(':5000', start)
                    sf_dict['service-functions']['service-function'][index_sf]['rest-uri'] = sf_dict['service-functions']['service-function'][index_sf]['rest-uri'].replace(
                        sf_dict['service-functions']['service-function'][index_sf]['rest-uri'][start:end], new_data[sff['service-node']]['first_address'])
                else:
                    sf_dict['service-functions']['service-function'][index_sf]['rest-uri'] = 'http://' + new_data[sff['service-node']]['first_address'] + ':5000'


            index_sf+=1
            '''For SFC-ODL Lithium'''
            #for i in range(0, len(sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['service-function-dictionary'])):
            #    sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['service-function-dictionary'][i]['sff-sf-data-plane-locator']['ip'] = new_data[sff['service-node']]['first_address']
            for i in range(0, len(sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['sff-data-plane-locator'])):
                sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['sff-data-plane-locator'][i]['data-plane-locator']['ip'] = new_data[sff['service-node']]['first_address']
            if sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['rest-uri']:
                start = sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['rest-uri'].find('http://') + 7
                end = sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['rest-uri'].find(':5000', start)
                sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['rest-uri'] = sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['rest-uri'].replace(
                    sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['rest-uri'][start:end], new_data[sff['service-node']]['first_address'])
            else:
                sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['rest-uri'] = 'http://' + new_data[sff['service-node']]['first_address'] + ':5000'


            sff_dict['service-function-forwarders']['service-function-forwarder'][index_sff]['ip-mgmt-address'] = \
            new_data[sff['service-node']]['first_address']

        index_sff+=1


    sf_sff_template = {}
    sf_sff_template['sf'] = json.dumps(sf_dict)
    sf_sff_template['sff'] = json.dumps(sff_dict)


    return sf_sff_template




def request_decomposition(tosca, translator, stack_name, save_file):

    sfc_resources = ['tosca.nodes.nfv.CP', 'tosca.nodes.nfv.VL', 'tosca.nodes.nfv.VNF', 'tosca.nodes.nfv.FP', 'tosca.nodes.nfv.VNFFG']
    sfc_template = False

    #************************************************************************************************************#
    #                                                                                                            #
    #           Network Connectivity Topology template translation to HEAT Orchestration Template                #
    #               Network Connectivity Topology template instantiation via HEAT Client API                     #
    #                                                                                                            #
    #************************************************************************************************************#
    nct_template = HotTemplate()
    nct_template.description = translator.hot_template.description
    nct_template.parameters = translator.hot_template.parameters
    nct_template.outputs = translator.hot_template.outputs
    nct_template.resources = []
    for resource in translator.hot_template.resources:
        if resource.type not in sfc_resources:
            nct_template.resources.append(resource)
        else:
            sfc_template = True

    if save_file:
        nct_file = open("nct_" + stack_name + ".yml", "w")
        nct_file.write(nct_template.output_to_yaml())
        nct_file.close()


    request_resources = {}


    template_decomposition = {}
    template_decomposition['nct'] = nct_template.output_to_yaml()

    nct_output_dict = dict((x.name, x.__dict__) for x in nct_template.outputs)
    template_decomposition['output'] = json.dumps(nct_output_dict)

    #************************************************************************************************************#
    #                                                                                                            #
    #                           VNF Forwarding Graph construction and creation                                   #
    #                                                                                                            #
    #************************************************************************************************************#

    if sfc_template:
        service_functions = {}
        service_functions['service-functions'] = {}
        service_function = []


        service_function_forwarders = {}
        service_function_forwarders['service-function-forwarders'] = {}
        service_function_forwarder = []

        service_function_chains = {}
        service_function_chains['service-function-chains'] = {}
        service_function_chain = []

        service_function_paths = {}
        service_function_paths['service-function-paths'] = {}
        service_function_path = []

        rendered_service_path = {}
        rendered_service_path['input']={}


        for resource in translator.hot_template.resources:
            if (resource.type == 'tosca.nodes.nfv.CP'):
                service_function_forwarder.append(resource.properties)
            if (resource.type == 'tosca.nodes.nfv.VNF'):
                del resource.properties['server']
                service_function.append(resource.properties)
            if (resource.type == 'tosca.nodes.nfv.FP'):
                service_function_chain.append(resource.properties)
                fps = {}
                fps['name'] = resource.properties['name']
                fps['service-chain-name'] = resource.properties['name']
                fps['symmetric'] = True
                rendered_service_path['input']['parent-service-function-path'] = resource.properties['name']
                service_function_path.append(fps)
        service_functions['service-functions']['service-function'] = service_function
        service_function_forwarders['service-function-forwarders']['service-function-forwarder'] = service_function_forwarder
        service_function_chains['service-function-chains']['service-function-chain'] = service_function_chain
        service_function_paths['service-function-paths']['service-function-path'] = service_function_path



        for node in tosca.nodetemplates:
            if node.type == 'tosca.nodes.Compute':
                request_resources[node.name] = node.entity_tpl['capabilities']['host']['properties']



        j = 0
        for node in tosca.nodetemplates:
            if node.type == 'tosca.nodes.nfv.FP':
                for cp in node.requirements:
                    for resource in translator.hot_template.resources:
                        if (resource.type == 'tosca.nodes.nfv.CP'):
                            if resource.properties['name'] == cp['forwarder']:
                                for res in request_resources:
                                    if res == resource.properties['service-node']:
                                        request_resources[res]['order']=j
                                        j+=1



        '''i = 0
        for node in tosca.nodetemplates:
            if node.type == 'tosca.nodes.nfv.FP':
                for cp in node.requirements:
                    #print cp['forwarder']
                    for resource in translator.hot_template.resources:
                        if (resource.type == 'tosca.nodes.nfv.CP'):
                            if resource.properties['name'] == cp['forwarder']:
                                #print resource.properties['service-node']
                                for res in request_resources.resources:
                                    if res.name == resource.properties['service-node']:
                                        res.properties['order']=i
                                        i+=1
                                        #print res.properties'''


        if save_file:
            sf_file = open("sf_" + stack_name + ".json", "w")
            sff_file = open("sff_" + stack_name + ".json", "w")
            sfc_file = open("sfc_" + stack_name + ".json", "w")
            sfp_file = open("sfp_" + stack_name + ".json", "w")
            rsp_file = open("rsp_" + stack_name + ".json", "w")

            sf_file.write(json.dumps(service_functions))
            sff_file.write(json.dumps(service_function_forwarders))
            sfc_file.write(json.dumps(service_function_chains))
            sfp_file.write(json.dumps(service_function_paths))
            rsp_file.write(json.dumps(rendered_service_path))

            sf_file.close()
            sff_file.close()
            sfc_file.close()
            sfp_file.close()
            rsp_file.close()


        template_decomposition['sf'] = json.dumps(service_functions)
        template_decomposition['sff'] = json.dumps(service_function_forwarders)
        template_decomposition['sfc'] = json.dumps(service_function_chains)
        template_decomposition['sfp'] = json.dumps(service_function_paths)
        template_decomposition['rsp'] = json.dumps(rendered_service_path)
        template_decomposition['request'] = json.dumps(request_resources)#.output_to_yaml()



    if save_file:
        request_file = open("request_" + stack_name + ".yml", "w")
        request_file.write(request_resources.output_to_yaml())
        #request_file.write(request_resources)
        request_file.close()

    return template_decomposition