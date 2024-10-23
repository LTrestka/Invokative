
import sys
import functools
import inspect

from handler import METHODS, start_function, end_function
from brain import BRAIN

def track_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global BRAIN
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back

        # Get the function name being wrapped
        current_func_name = func.__name__
        
        # Determine the class and method of the current function
        current_class_name = None
        if 'self' in current_frame.f_locals:
            current_class_name = type(current_frame.f_locals['self']).__name__
        
        # Determine the class and method of the calling function
        caller_func_name = caller_frame.f_code.co_name
        caller_class_name = None
        
        if 'self' in caller_frame.f_locals:
            caller_class_name = type(caller_frame.f_locals['self']).__name__
        
        # Get or create lobe and neuron for the current function
        from_lobe = BRAIN.fetch_lobe(caller_class_name)
        from_neuron = BRAIN.fetch_neuron_by_name(from_lobe, caller_func_name)
        
        # Build the log message
        if caller_class_name:
            caller_info = f"{caller_class_name}.{caller_func_name}"
        else:
            caller_info = caller_func_name

        if current_class_name:
            current_info = f"{current_class_name}.{current_func_name}"
        else:
            current_info = current_func_name
            
        # Get or create lobe and neuron for the current function
        to_lobe = BRAIN.fetch_lobe(current_class_name)
        to_neuron = BRAIN.fetch_neuron_by_name(to_lobe, current_func_name)
        
        

        # Log the call relationship
        print(f"{caller_info} called {current_info}")
            
        
        id = start_function(func.__name__)
        start_time = METHODS[id]
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = end_function(id, func.__name__)
            BRAIN.add_synapse(from_neuron, to_neuron, start_time, end_time)
        return result
    return wrapper

