#!/usr/bin/env python3
import os
import sys
import oci

from operator import itemgetter
from oci.core import ComputeClient
from oci.core.models import LaunchInstanceDetails, ImageSourceDetails, CreateImageDetails


class Compute(object):

    def __init__(self, config_file):
        
        self.config_file = config_file

        #Check if config file exist
        if os.path.isfile(self.config_file):
            try:
                self.config = oci.config.from_file(self.config_file)
            except Exception as err:
                raise err
        else:
            raise Exception("config file is required")

        #Compute client
        self.client = ComputeClient(self.config)

    def _latest_avail_image(self, name):

        #find latest available image
        resp = self.client.list_images(self.config['compartment_id'],
            display_name=name,
            sort_by="TIMECREATED",
            sort_order="DESC" 
        )
        return resp.data[0]
    
    def get_all_images(self, name):

        #find latest available image
        resp = self.client.list_images(self.config['compartment_id'],
            sort_by="TIMECREATED",
            sort_order="DESC" 
        )
        imgs = []
        for img in resp.data:
            i = {}
            if name in img.display_name:
                i['display_name'] = img.display_name
                i['id'] = img.id
                i['time_created'] = img.time_created
                imgs.append(i)
        return sorted(imgs, key=itemgetter('time_created'), reverse=True)
    
    def _avail_shapes(self, img_id):

        resp = self.client.list_shapes(
            self.config['compartment_id'],
            availability_domain=self.config['ad'],
            image_id=img_id
            )
        return resp.data[0].shape

        
    def create_instance(self, img_name, env=None, owner=None):
        """
        Create a DB instance based on latest available image
        """
        #find latest image available
        img_id = self._latest_avail_image(img_name).id
        
        #instance details
        if env is not None and owner is not None:
            dn = "db_" + env + "_" + owner
        elif env == "qa":
            dn = "db_QA"
        else:
            dn = "db_instance"

        instance_details = LaunchInstanceDetails(
            availability_domain=self.config['ad'],
            compartment_id=self.config['compartment_id'],
            freeform_tags={"owner":owner, "environment":env},
            display_name=dn,
            image_id=img_id,
            shape=self._avail_shapes(img_id),
            subnet_id=self.config['subnetid']
        )

        try:
            self.client.launch_instance(instance_details)
            print("instance is creating")
        except Exception as err:
            raise err
    
    def _find_serv(self, srv_name):

        resp = self.client.list_instances(
            compartment_id=self.config['compartment_id'],
            display_name=srv_name
        )
        return resp.data
    
    def delete_instance(self, srv_name):

        try:
            srv_id = self._find_serv(srv_name)[0].id
        except Exception:
            print("No server with name " + srv_name + " has been found")
            return
        
        self.client.terminate_instance(instance_id=srv_id)
        print("instance " + srv_name + " is going to be deleted")
    
    def manage_instance(self, srv_name, srv_action, dry_run=False):

        if dry_run:
            return "Dry run is enable if not this would work"
        #find server
        server_id = self._find_serv(srv_name)[0].id

        if srv_action == "delete":
            try:
                self.client.terminate_instance(
                    instance_id=server_id
                )
                print("Server with name: " + srv_name + " will be deleted")
            except Exception as err:
                raise err
        else:
            try:
                self.client.instance_action(
                    instance_id=server_id,
                    action=srv_action.upper()
                )
            except Exception as err:
                raise err
    
    def create_image(self, srv_name, img_name):

        try:
            srv_id = self._find_serv(srv_name)[0].id
        except Exception:
            print("No server with name " + srv_name + " has been found")
            return

        image_details = CreateImageDetails(
            compartment_id=self.config['compartment_id'],
            display_name=img_name,
            freeform_tags={"name":img_name},
            instance_id=srv_id
        )

        try:
            self.client.create_image(image_details)
            print("image is creating")
        except Exception as err:
            raise err




    
    

        



    