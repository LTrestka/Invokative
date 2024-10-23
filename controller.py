import os

from argparse import ArgumentParser, RawTextHelpFormatter
from unittest import runner
from globals import OUTPUT_DIR, OUTPUT_TYPE, PROGRAM_NAME, RECURSIVE, get_workdir
from handler import end_node, set_config_file, start_node, write_message, dump_node_messages
  


ARGS = None
def parse_key_value_pair(s):
    """Helper function to parse key=value pairs."""
    key, value = s.split('=', 1)
    return key, value


class Controller(ArgumentParser):
    def __init__(self):
        self.input = ArgumentParser(description='Application Flow Chart', formatter_class=RawTextHelpFormatter)
        self._set_default_args()
        
    def _set_default_args(self):
        global VERBOSE, RECURSIVE, OUTPUT_DIR, OUTPUT_TYPE
        self.input.add_argument('-r','--recursive', action='store_true', default=RECURSIVE, help='Recursively tracks execution on all modules and their submodules, as deep as it can')
        self.input.add_argument('-v','--verbose', action='store_true', default=VERBOSE, help='Verbose output')
        self.input.add_argument('-t','--output_type', default=OUTPUT_TYPE, required=False, help='Specify format for generated output')
        self.input.add_argument('-o','--output_path', default=OUTPUT_DIR, required=False, help='Specify path for generated output')
    
    def _add_configuration_settings(self):
        config_group = self.input.add_mutually_exclusive_group("cfg", "config", title="Configuration Settings", description="Options regarding configuration.")
        config_group.add_argument(
            '-g',
            '--get',
            type=str,
            required=False,
            help='Get Configuration Item'
        )
        config_group.add_argument(
            '-s',
            '--set',
            action='append', 
            type=parse_key_value_pair,
            help="Set key=value pairs (can be used multiple times)",
            metavar="KEY=VALUE",
            required=False,
            help='Set Configuration Item, e.g., -s key1=value1 --set key2=value2'
        )
        config_group.add_argument(
            '-f',
            '--file', 
            type=str, 
            default=f"{get_workdir()}/{PROGRAM_NAME}.yaml",
            help="Output directory for config files."
        )
        
        
        
    def initialize_args(self):
        global VERBOSE, RECURSIVE, OUTPUT_DIR, OUTPUT_TYPE
        args, other_args = self.input.parse_known_args()
        ARGS = args
        return ARGS
    

        
        
        

        


   