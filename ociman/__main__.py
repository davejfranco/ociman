import sys
from ociman.cli import args
from ociman.compute import Instance



def main():
     #Load arguments
    parser = args(sys.argv[1:])
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    else:
        arg = parser.parse_args(sys.argv[1:])
    


    # #Create Instance
    if arg.create_instance and arg.image_name is not None:
        db.create_instance(arg.image_name, arg.env, arg.own)
        sys.exit(0)


if __name__ == "__main__":
    main()
   
    
    