import os
import sys
import oci
from pathlib import Path
from operator import itemgetter
from source.clients import Clients
from oci.core.models import LaunchInstanceDetails, ImageSourceDetails, CreateImageDetails


class Compute:

    def __init__(self, config_path, profile, compartment_id):
        
        self.config_path = config_path
        self.profile = profile
        self.compatment_id = compartment_id

        #Compute Client
        self.ccli = Clients(self.config_path, self.profile).compute()
   
        

    def list_vms_by_tag(self, tag_key, tag_value):
        
        response = self.ccli.list_instances(self.compatment_id)
        allvms = response.data
        foundvms = []

        for vm in allvms:
            if tag_key in vm.freeform_tags and vm.freeform_tags[tag_key] == tag_value:
                foundvms.append(vm.id)       
        return foundvms

    def manage_instance(self, Operation, instance_ids):
        
        valid_ops = ["STOP", "START", "SOFTRESET", "RESET", "SOFTSTOP"]
        if Operation in valid_ops:
            for vmid in instance_ids:
                self.ccli.instance_action(vmid, Operation)
        else:
            print(f"Not a valid action {Operation}")
 
    

    # def _latest_avail_image(self, name):

    #     #find latest available image
    #     resp = self.ccli.list_images(self.config['compartment_id'],
    #         display_name=name,
    #         sort_by="TIMECREATED",
    #         sort_order="DESC" 
    #     )
    #     return resp.data[0]
    
    # def get_all_images(self, name):

    #     #find latest available image
    #     resp = self.ccli.list_images(self.config['compartment_id'],
    #         sort_by="TIMECREATED",
    #         sort_order="DESC" 
    #     )
    #     imgs = []
    #     for img in resp.data:
    #         i = {}
    #         if name in img.display_name:
    #             i['display_name'] = img.display_name
    #             i['id'] = img.id
    #             i['time_created'] = img.time_created
    #             imgs.append(i)
    #     return sorted(imgs, key=itemgetter('time_created'), reverse=True)
    
    # def _avail_shapes(self, img_id):

    #     resp = self.ccli.list_shapes(
    #         self.config['compartment_id'],
    #         availability_domain=self.config['ad'],
    #         image_id=img_id
    #         )
    #     return resp.data[0].shape

        
    # def create_instance(self, img_name, env=None, owner=None):
    #     """
    #     Create a DB instance based on latest available image
    #     """
    #     #find latest image available
    #     img_id = self._latest_avail_image(img_name).id
        
    #     #instance details
    #     if env is not None and owner is not None:
    #         dn = "db_" + env + "_" + owner
    #     elif env == "qa":
    #         dn = "db_QA"
    #     else:
    #         dn = "db_instance"

    #     instance_details = LaunchInstanceDetails(
    #         availability_domain=self.config['ad'],
    #         compartment_id=self.config['compartment_id'],
    #         freeform_tags={"owner":owner, "environment":env},
    #         display_name=dn,
    #         image_id=img_id,
    #         shape=self._avail_shapes(img_id),
    #         subnet_id=self.config['subnetid']
    #     )

    #     try:
    #         self.client.launch_instance(instance_details)
    #         print("instance is creating")
    #     except Exception as err:
    #         raise err
    
    # def _find_serv(self, srv_name):

    #     resp = self.client.list_instances(
    #         compartment_id=self.config['compartment_id'],
    #         display_name=srv_name
    #     )
    #     return resp.data
    
    # def delete_instance(self, srv_name):

    #     try:
    #         srv_id = self._find_serv(srv_name)[0].id
    #     except Exception:
    #         print("No server with name " + srv_name + " has been found")
    #         return
        
    #     self.client.terminate_instance(instance_id=srv_id)
    #     print("instance " + srv_name + " is going to be deleted")
    
    # def manage_instance(self, srv_name, srv_action, dry_run=False):

    #     if dry_run:
    #         return "Dry run is enable if not this would work"
    #     #find server
    #     server_id = self._find_serv(srv_name)[0].id

    #     if srv_action == "delete":
    #         try:
    #             self.client.terminate_instance(
    #                 instance_id=server_id
    #             )
    #             print("Server with name: " + srv_name + " will be deleted")
    #         except Exception as err:
    #             raise err
    #     else:
    #         try:
    #             self.client.instance_action(
    #                 instance_id=server_id,
    #                 action=srv_action.upper()
    #             )
    #         except Exception as err:
    #             raise err
    
    # def create_image(self, srv_name, img_name):

    #     try:
    #         srv_id = self._find_serv(srv_name)[0].id
    #     except Exception:
    #         print("No server with name " + srv_name + " has been found")
    #         return

    #     image_details = CreateImageDetails(
    #         compartment_id=self.config['compartment_id'],
    #         display_name=img_name,
    #         freeform_tags={"name":img_name},
    #         instance_id=srv_id
    #     )

    #     try:
    #         self.client.create_image(image_details)
    #         print("image is creating")
    #     except Exception as err:
    #         raise err




    
    

        



    