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

class Compute_node:


    def __init__(self, infrastructure):
        self.inf = infrastructure
          
    def get_ip_add(self,compute_name):
        ip_address=self.inf.find_compute_node_by_name(compute_name).host_ip
        return ip_address

    def get_list_of_VMs_of_compute_node(self,compute_name):
        list=[]
        if self.inf.if_exist_compute_node_by_name(compute_name):
           for instance in self.inf.nova_authentification().servers.list(search_opts={'all_tenants':1}):
               if compute_name == getattr(instance, 'OS-EXT-SRV-ATTR:hypervisor_hostname'):
                  list.append(instance)
           return list

    def get_name_of_VMs_of_compute_node(self, compute_name):
        list=[]
        for vm in self.get_list_of_VMs_of_compute_node(compute_name):
            list.append(vm.name)
        return list


##################################### Nova_resources ##################################
    def get_nova_resources(self,compute_name):
       nova_resources=self.inf.find_compute_node_by_name(compute_name).__dict__
       total_cpu=nova_resources["vcpus"]
       total_res_disk_size=nova_resources["local_gb"]
       total_memory_size=nova_resources["memory_mb"]
       cpu_used = nova_resources["vcpus_used"]
       free_c=total_cpu - cpu_used
       if free_c>0:
          free_cpu=free_c
       else:
          free_cpu=0
       free_d = nova_resources["free_disk_gb"]
       if free_d>0:
          free_disk=free_d
       else:
          free_disk=0
       free_mem = nova_resources["free_ram_mb"]
       resources={"total_CPU":total_cpu,"total_res_disk_size":total_res_disk_size,"total_memory_size":total_memory_size, "free_cpu":free_cpu,"free_disk":free_disk,"free_mem":free_mem}
       
       return resources

#################################### SNMP_resources ###################################
    def get_CPU_load(self,compute_name):

        server = self.inf.find_compute_node_by_name(compute_name)
        query_compute = [dict(field='resource_id', op='eq', value=server.host_ip)]

        cpu_load_1m = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.cpu.load.1min',
                                                             limit=1, q=query_compute)
        cpu_load_5m = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.cpu.load.5min',
                                                             limit=1, q=query_compute)
        cpu_load_15m = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.cpu.load.15min',
                                                          limit=1, q=query_compute)

        cpu_load={"hardware.cpu.load.1min (PROCESS)":cpu_load_1m[0].counter_volume,
                  "hardware.cpu.load.5min (PROCESS)":cpu_load_5m[0].counter_volume,
                  "hardware.cpu.load.15min (PROCESS)":cpu_load_15m[0].counter_volume}
        return cpu_load

    def get_memory_metrics(self, compute_name):
        server = self.inf.find_compute_node_by_name(compute_name)
        query_compute = [dict(field='resource_id', op='eq', value=server.host_ip)]

        mem_tot = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.memory.total', limit=1,
                                                               q=query_compute)
        mem_avail = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.memory.used', limit=1,
                                                              q=query_compute)
        swap_tot = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.memory.swap.total', limit=1,
                                                              q=query_compute)
        swap_avail = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.memory.swap.avail', limit=1,
                                                                q=query_compute)
        memory={"memory.total (KB)":mem_tot[0].counter_volume,
                "memory_available (KB)": mem_avail[0].counter_volume,
                "memory.swap.total (KB)":swap_tot[0].counter_volume,
                "memory.swap.available (KB)" :swap_avail[0].counter_volume}
        return memory

    def get_compute_system_metrics(self,compute_name):
        server = self.inf.find_compute_node_by_name(compute_name)
        query_compute = [dict(field='resource_id', op='eq', value=server.host_ip)]
        sys_in_block = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.system_stats.io.incoming.blocks',
                                                                  limit=1, q=query_compute)
        sys_out_block = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.system_stats.io.outgoing.blocks',
                                                                   limit=1, q=query_compute)
        sys_cpu_idle = self.inf.ceilometer_authentification().samples.list(meter_name='hardware.system_stats.cpu.idle',
                                                                      limit=1, q=query_compute)

        system={"system_stats.io.incoming.blocks (BLOCKS)":sys_in_block[0].counter_volume,
                "system_stats.io.outgoing.blocks (BLOCKS)":sys_out_block[0].counter_volume,
                "system_stats.cpu.idle (%)":sys_cpu_idle[0].counter_volume }

        return system


#################################### Network_resources ##############################

    def get_compute_network_metrics(self,compute_name):

        server = self.inf.find_compute_node_by_name(compute_name)
        query_compute = [dict(field='resource_id', op='eq', value=server.host_ip)]
        net_ip_in_datag = self.inf.ceilometer_authentification().samples.list( meter_name='hardware.network.ip.incoming.datagrams',
                                                                                 limit=1, q=query_compute)
        net_ip_out_datag = self.inf.ceilometer_authentification().samples.list( meter_name='hardware.network.ip.outgoing.datagrams',
                                                                                  limit=1, q=query_compute)

        net_met={"hardware.network.ip.incoming.datagrams (DATAGRAMS)":net_ip_in_datag[0].counter_volume,
                 "hardware.network.ip.outgoing.datagrams (DATAGRAMS)":net_ip_out_datag[0].counter_volume}

        return net_met


#######################################################################################

    def get_total_CPU(self,compute_name):
        total_cpu = self.inf.find_compute_node_by_name(compute_name).vcpus
        return total_cpu

    def get_total_res_disk_size(self, compute_name):
        total_disk = self.inf.find_compute_node_by_name(compute_name).local_gb
        return total_disk

    def get_total_memory_size(self, compute_name):
        total_mem = self.inf.find_compute_node_by_name(compute_name).memory_mb
        return total_mem


    def get_free_CPU_hyp(self,compute_name):
        total_cpu = self.inf.find_compute_node_by_name(compute_name).vcpus
        cpu_used = self.inf.find_compute_node_by_name(compute_name).vcpus_used
        free_cpu=total_cpu - cpu_used
        if free_cpu>0:
          return free_cpu
        else: return 0



    def get_free_res_disk(self,compute_name):
        free_disk = self.inf.find_compute_node_by_name(compute_name).free_disk_gb
        if free_disk<=0:
           free_disk=0
        return free_disk

    def get_free_res_memory(self,compute_name):
        free_mem = self.inf.find_compute_node_by_name(compute_name).free_ram_mb
        return free_mem