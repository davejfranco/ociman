#!/usr/bin/env python3
import os
import oci
from oci.core import ComputeClient
from oci.core.models import LaunchInstanceDetails, ImageSourceDetails


class Database(object):

    def __init__(self, config_file):
        
        self.config_file = config_file

        #Check if config file exist
        if os.path.isfile(self.config_file):
            try:
                self.config = oci.config.from_file(self.config_file)
            except Exception as err:
                raise err
        else:
            try:
                self.config = oci.config.from_file(CONFIGFILE)
            except Exception as err:
                raise err

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
    
    def _avail_shapes(self, img_id):

        resp = self.client.list_shapes(
            self.config['compartment_id'],
            availability_domain=self.config['ad'],
            image_id=img_id
            )
        return resp.data[0].shape

        
    def create(self, img_name, env, owner):
        """
        Create a DB instance based on latest available image
        """
        #find latest image available
        img_id = self._latest_avail_image(img_name).id
        #instance details
        instance_details = LaunchInstanceDetails(
            availability_domain=self.config['ad'],
            compartment_id=self.config['compartment_id'],
            defined_tags={"poc":{"owner":owner, "environment":env}},
            display_name=env + "_db_" + owner,
            image_id=img_id,
            shape=self._avail_shapes(img_id),
            subnet_id=self.config['subnetid']
        )

        try:
            self.client.launch_instance(instance_details)
        except Exception as err:
            raise err

    
    

        



    