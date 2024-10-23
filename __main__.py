import sys
import builtins

from controller import Controller
from decorator import track_execution
from globals import end_run, start_run


runner_mod = sys.modules["runner"]
parser_mod = sys.modules["controller"]
global_mod = sys.modules["globals"]

modules_to_decorate = [runner_mod, parser_mod]

def apply_decorator_to_methods(obj):
    """Recursively apply the track_execution decorator to all callable functions and class methods."""
    for name, item in obj.__dict__.items():
        if isinstance(item, (type, int, str, list, dict, set, float, complex, tuple, bool, bytes)):
            continue
        elif isinstance(item, type):
            #print(f"Found class: {name}, decorating its methods")
            apply_decorator_to_methods(item)
        elif callable(item)  and "." not in name and name not in ["__init__","log", "write_message", "dump_node_messages", "end_node", "start_node", "start_run", "end_run"]:
            #print(f"Decorating function/method: {name}")
            setattr(obj, name, track_execution(item))

for module in modules_to_decorate:
    #print(f"Decorating module: {module.__name__}")
    apply_decorator_to_methods(module)
    
ctrl = Controller()
start_run()
ctrl.run()
end_run()