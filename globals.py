import os

def get_workdir():
    return os.path.dirname(os.path.abspath(__file__))

PROGRAM_NAME="appmapp"
VERBOSE = False
RECURSIVE=True
OUTPUT_TYPE="json"
OUTPUT_DIR=f"{get_workdir()}/output"
CONFIG_FILE=f"{get_workdir()}/appmap.yaml"