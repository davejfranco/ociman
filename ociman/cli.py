import sys
import argparse
from pathlib import Path
from ociman.compute import Instance


def args(args=None):

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

