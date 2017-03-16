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

from novaclient import client
import ceilometerclient.client
import novaclient
from packaging import version as pack_version
class Infrastructure:


    def __init__(self, version, username, password, tenant_name, tenant_id, endpoint, service, region):
        self.version = version
        self.username = username
        self.password = password
        self.tenant_name = tenant_name
        self.tenant_id = tenant_id
        self.endpoint = endpoint
        self.service = service
        self.region = region


    ###### Authenticate in Nova
    def nova_authentification(self):
        if pack_version.parse(novaclient.__version__) < pack_version.parse("7.0.0"):
            nova_client = client.Client(self.version, self.username, self.password,
                                    self.tenant_name, self.endpoint,
                                service_type=self.service,
                                region_name=self.region)
        else:
            nova_client = client.Client(self.version, self.username, self.password,
                                        self.tenant_id, self.endpoint,
                                        service_type=self.service,
                                        region_name=self.region)
        return nova_client

    ##### Authenticate in Ceilometer
    def ceilometer_authentification(self):
        ceilometer_client = ceilometerclient.client.get_client(2, os_username=self.username,
                                                 os_password=self.password,
                                                 os_tenant_name=self.tenant_name,
                                                 os_auth_url=self.endpoint)
        return ceilometer_client


    def get_compute_nodes_list(self):
        hypervisor_list = self.nova_authentification().hypervisors.list()
        return hypervisor_list

    def get_number_compute_nodes(self):
        return self.get_compute_nodes_list().__len__()

    def get_compute_nodes_ip_list(self):
        list = []
        for hyp in self.get_compute_nodes_list():
            list.append(hyp.host_ip)
        return list

    def get_compute_nodes_name_list(self):
        list = []
        for hyp in self.get_compute_nodes_list():
            list.append(hyp.service['host'])
            #list.append(hyp.hypervisor_hostname)
        return list

    def if_exist_compute_node_by_ip(self,hypervisor_ip):
        list = self.get_compute_nodes_ip_list()
        exist = False
        if hypervisor_ip in list:
            exist = True
        return exist

    def if_exist_compute_node_by_name(self,hypervisor_name):
        list = self.get_compute_nodes_name_list()
        exist = False
        if hypervisor_name in list:
            exist = True
        return exist

    def find_compute_node_by_name(self,hypervisor_name):
        list = self.get_compute_nodes_list()
        for i in range(0, list.__len__()):
            #if list[i].hypervisor_hostname == hypervisor_name:
            if list[i].service['host'] == hypervisor_name:
                return list[i]


    def find_compute_node_by_ip(self,hypervisor_ip):
        list = self.get_compute_nodes_list()
        for i in range(0, list.__len__()):
            if list[i].host_ip == hypervisor_ip:
                return list[i]

    def get_list_of_idle_compute_nodes(self):
        list = []
        for hypervisor in self.get_compute_nodes_list():
            if hypervisor.running_vms == 0:
                #list.append(hypervisor.hypervisor_hostname)
                list.append(hypervisor.service['host'])
        return list

    def get_number_of_idle_compute_nodes(self):
        return self.get_list_of_idle_compute_nodes().__len__()

    def get_percentage_used_compute_nodes(self):
        average_host = float(self.get_number_compute_nodes() - self.get_number_of_idle_compute_nodes())
        return (average_host / self.get_number_compute_nodes()) * 100