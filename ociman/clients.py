import os
import sys
import oci
from pathlib import Path
from oci.identity import IdentityClient
from oci.core import ComputeClient

class OciConfig:

    def __init__(self, config_path, profile):
        self.config_path = config_path
        self.profile = profile

        if os.path.isfile(self.config_path):
            try:
                if oci.config.validate_config(self.config_path):
                    self.config = oci.config.from_file(self.config_path, self.profile)
                else:
                    raise oci.exceptions.InvalidConfig
            except oci.exceptions.ConfigFileNotFound as err:
                print(err, file=sys.stderr)
                sys.exit(1)
            except Exception as err:
                print(err, file=sys.stderr)
                sys.exit(1)
        else:
            print(f"No file found on provided config path {self.config_path}")
            sys.exit(1)  
    
    def add_compartment(self, compartment_id):
        self.config['compartment_id'] = compartment_id

class Clients(OciConfig):

    def __init__(self, config_path=str(Path.home())+'/.oci/config', profile='DEFAULT'):
        super().__init__(config_path, profile)

    def compute(self):    
        
        try:
            return ComputeClient(self.config)
        except oci.exceptions.ClientError as err:
            print(err, file=sys.stderr)
            sys.exit(1)
    
    def identity(self, region=None):    
        try:
            return IdentityClient(self.config)
        except oci.exceptions.ClientError as err:
            print(err, file=sys.stderr)
            sys.exit(1)
