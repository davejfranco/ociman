import sys
from pathlib import Path
from ociman.cli import args, tag_validator
from ociman.compute import Instance



def main():
     #Load arguments
    parser = args(sys.argv[1:])
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    else:
        arg = parser.parse_args(sys.argv[1:])
    
    #Intance creation
    cli = Instance(arg.config, arg.profile, arg.cid)
    
    #manage instance
    if arg.action and arg.tag:
        if not tag_validator(arg.tag):
            sys.exit(0)
        keyvalue = arg.tag.split(":")
        #instances = cli.list_vms_by_tag(keyvalue[0],keyvalue[1])
        cli.manage_instance(arg.action.upper(), keyvalue[0],keyvalue[1])
        sys.exit(0)
    
    #list Instances with given freeform tag
    if arg.list and arg.tag:
        if not tag_validator(arg.tag):
            print("Not a valid tag")
            sys.exit(0)
        
        keyvalue = arg.tag.split(":")
        cli.instances_pretty_print(keyvalue[0],keyvalue[1])


if __name__ == "__main__":
    """
    Main entrypoint
    """
    main()
   
    
    