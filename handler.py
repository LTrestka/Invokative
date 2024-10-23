from datetime import datetime
import socket
import sys
import uuid

from brain import initialize_brain, BRAIN


HOSTNAME = socket.gethostname()
CURRENT_HOST = socket.gethostname()

RUN_START = datetime.now()

MODULES = {}
CLASSES = {}
METHODS = {}
TOTAL_METHOD_CALLS = 0

NAME_ID_IDX= {}
NAME_CLASS_IDX = {}
PATHS = {}
LOGS = []

def start_run():
    global RUN_START, HOSTNAME
    initialize_brain()
    RUN_START = datetime.now()
    HOSTNAME = socket.gethostname()
    
def end_run():
    global RUN_START, BRAIN
    print(f"RUN_START Complete | {timestamps(section=False)}")
    BRAIN.draw_brain()
    sys.exit(0)
        
def dump_logs(node=None):
    global NODE_MESSAGES, CURRENT_HOST
    node = node if node else CURRENT_HOST
    if not node or node not in NODE_MESSAGES:
        return
    for msg in NODE_MESSAGES[node]:
        print(f"|                 >> {msg}")
    NODE_MESSAGES[node] = []
        
def write_message(msg):
    global NODE_MESSAGES, CURRENT_HOST
    if not CURRENT_HOST:
        CURRENT_HOST = HOSTNAME
    if not NODE_MESSAGES:
        NODE_MESSAGES={}
    if CURRENT_HOST not in NODE_MESSAGES:
        NODE_MESSAGES[CURRENT_HOST] = []
    NODE_MESSAGES[CURRENT_HOST].append(msg)
    
    
def runtime(time):
    runtime = (datetime.now() - time)
    if runtime.seconds > 1:
        return f"{runtime.seconds}.{runtime.microseconds // 100}s"
    return f"{runtime.seconds}.{runtime.microseconds // 10}s"

def get_function_length():
    global METHODS
    length = len(METHODS)
    return length

LAST_SPACING = None
def get_last_spacing(complete = False):
    global LAST_SPACING
    base_padding = "|        "
    retval = ""
    padding = len(METHODS)
    if LAST_SPACING is not None:
        if bool(LAST_SPACING < padding):
            retval = ((padding -1) * "  ") + '->' 
        elif bool(LAST_SPACING > padding):
            retval = (padding * "  ") + '<-'
        else:
            retval = (padding * "  ") + "  "
        
         
    LAST_SPACING = padding
    return base_padding + retval
    

def start_function(function_name):
    global METHODS, TOTAL_METHOD_CALLS
    TOTAL_METHOD_CALLS += 1
    id = uuid.uuid4()
    METHODS[id] = datetime.now()
    #spacing = get_last_spacing()
    #print(f"{spacing}    -{TOTAL_METHOD_CALLS}: {function_name}: Begin")
    return id, METHODS[id]

def end_function(id, function_name):
    global METHODS, TOTAL_METHOD_CALLS
    spacing = get_last_spacing(len(METHODS))
    timestamp = timestamps(id)
    print(f"{spacing}    p-{TOTAL_METHOD_CALLS}: {function_name}(): {timestamp}")
    del METHODS[id]
    return timestamp

def timestamps(connection = None, section = True):
    global CURRENT_HOST, METHODS, CLASSES, RUN_START
    retval = {}
    if connection:
        retval.update({"connection": runtime(METHODS[connection])})
    if section:
        retval.update({"section": runtime(runtime(CLASSES[CURRENT_HOST]))})
    retval.update({"total": {runtime(RUN_START)}})
    return retval