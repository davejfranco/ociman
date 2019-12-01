#!/usr/bin/env python3
import sys
import argparse
from .ociman import Compute


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

# if __name__ == "__main__":

#     #Load arguments
#     parser = check_arg(sys.argv[1:])
#     if len(sys.argv) < 2:
#         parser.print_help()
#         sys.exit(0)
#     else:
#         arg = parser.parse_args(sys.argv[1:])
#     #print(arg)
#     #Load database class
#     db = Database(os.getcwd()+'/config')

#     # #Create Instance
#     if arg.create_instance and arg.image_name is not None:
#         db.create_instance(arg.image_name, arg.env, arg.own)
#         sys.exit(0)
    
#     # #Create Image
#     if arg.create_image and arg.server_name is not None and arg.image_name is not None:
#         db.create_image(arg.server_name, arg.image_name)
#         sys.exit(0)
    
#     # #Delete Instance
#     if arg.action == 'delete' and arg.server_name is not None:
#         db.delete_instance(arg.server_name)
#         sys.exit(0)
    
#     elif arg.action == 'start' or arg.action == "stop" and arg.server_name is not None:
#         db.manage_instance(arg.server_name, arg.action, arg.dry_run)
#         sys.exit(0)
#     else:
#         parser.print_help()
        