import os
import sys
import oci
from pathlib import Path
from operator import itemgetter
from ociman.clients import Clients
from oci.core.models import LaunchInstanceDetails, ImageSourceDetails, CreateImageDetails


class Instance:

    def __init__(self, config_path, profile, compartment_id):
        
        self.config_path = config_path
        self.profile = profile
        self.compatment_id = compartment_id

        #Compute Client
        self.ccli = Clients(self.config_path, self.profile).compute()       

    def _list_vms_by_tag(self, tag_key, tag_value):
        """
        Get all instance ocid by freeform tag key/value pair
        """
        response = self.ccli.list_instances(self.compatment_id)
        allvms = response.data
        foundvms = []

        for vm in allvms:
            if tag_key in vm.freeform_tags and vm.freeform_tags[tag_key] == tag_value:
                foundvms.append(vm)       
        return foundvms
    
    def _list_vm_ids(self, tag_key, tag_value):

        ids = []
        instances = self._list_vms_by_tag(tag_key, tag_value)
        for vm in instances:
            ids.append(vm.id)       
        return ids

    
    # def instances_pretty_print(self, tag_key, tag_value):
    #     """
    #     Print list of instances ids
    #     """
    #     instance_ids = self._list_vms_by_tag(tag_key, tag_value)
    #     if len(instance_ids) == 0:
    #         print("Not instance found with key:{k} and value: {v} \n".format(k=tag_key, v=tag_value))
    #         sys.exit(0)
    #     titles = ["Display Name", "State", "OCID"]


    def manage_instance(self, Operation, tag_key, tag_value):
        
        valid_ops = ["STOP", "START", "SOFTRESET", "RESET", "SOFTSTOP"]
        if Operation in valid_ops:            
            instances_ids = self._list_vms_by_tag(tag_key, tag_value) #self._list_vms_by_tag(tag_key, tag_value)
            for vmid in instance_ids:
                self.ccli.instance_action(vmid, Operation)
        else:
            print(f"Not a valid action {Operation}")
 



    
    

        



    