#!/usr/bin/env python3
import os
import sys
import oci
import argparse
from oci.core import ComputeClient
from oci.core.models import LaunchInstanceDetails, ImageSourceDetails, CreateImageDetails


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

def check_arg(args=None):

    parser = argparse.ArgumentParser(description='script to manage compute instance on oci')
    parser.add_argument('-C', '--create-instance',
                        action='store_true',
                        default=False)
    parser.add_argument('-I', '--create-image',
                        help='create image from server name',
                        action='store_true',
                        default=False)
    parser.add_argument('-s', '--server-name',
                        help='server name',
                        action='store')
    parser.add_argument('-i', '--image-name',
                        help='image name',
                        action='store')
    parser.add_argument('-e', '--env',
                        help='environment of the resource to be created',
                        action='store',
                        default="dev")
    parser.add_argument('-o', '--own',
                        help='owner of the resource to be created',
                        action='store')
    parser.add_argument('-a', '--action',
                        help='action to be taken on instances: start, stop, delete')
    parser.add_argument('-r', '--dry-run',
                        help='owner of the resource to be created',
                        action='store_false',
                        default=False)

   
    return parser 

if __name__ == "__main__":

    #Load arguments
    parser = check_arg(sys.argv[1:])
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    else:
        arg = parser.parse_args(sys.argv[1:])
    #print(arg)
    #Load database class
    db = Database(os.getcwd()+'/config')

    # #Create Instance
    if arg.create_instance and arg.image_name is not None:
        db.create_instance(arg.image_name, arg.env, arg.own)
        sys.exit(0)
    
    # #Create Image
    if arg.create_image and arg.server_name is not None and arg.image_name is not None:
        db.create_image(arg.server_name, arg.image_name)
        sys.exit(0)
    
    # #Delete Instance
    if arg.action == 'delete' and arg.server_name is not None:
        db.delete_instance(arg.server_name)
        sys.exit(0)
    
    elif arg.action == 'start' or arg.action == "stop" and arg.server_name is not None:
        db.manage_instance(arg.server_name, arg.action, arg.dry_run)
        sys.exit(0)
    else:
        parser.print_help()
        


    
    






    
    

        



    