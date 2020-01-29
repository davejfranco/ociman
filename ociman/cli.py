import argparse
from pathlib import Path

def args(args=None):

    parser = argparse.ArgumentParser(description='script to manage compute instance on oci')
    parser.add_argument('-c', '--config',
                        default=str(Path.home()) + '/.oci/config',
                        help="default config should be in ~/.oci/config")
    parser.add_argument('-p', '--profile',
                        default="DEFAULT")                    
    parser.add_argument('-t', '--tag',
                        help="assing action to server with freeform_tags, Example: --tag environment:dev",
                        default="DEFAULT") 
    parser.add_argument('--cid',
                        help='compartment id')
    parser.add_argument('-a', '--action',
                        help='action to be taken on instances: start, stop, delete, sofstop, reset, sofreset')
    parser.add_argument('-l', '--list', action="store_true", default=True,
                        help='list vm resources based on tag, --tag is required')
    parser.add_argument('-r', '--dry-run',
                        help='owner of the resource to be created',
                        action='store_false',
                        default=False)
 
    return parser 

def tag_validator(tag):
    if len(tag.split(":")) < 2:
        print(f"Invalid tag format {tag}, expecting: [key]:[value]")
        return False
    return True