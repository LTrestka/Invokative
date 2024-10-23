from ast import Dict, List
from datetime import datetime, timedelta
import json
from typing import Set, Tuple
from uuid import uuid4, UUID

from matplotlib.patches import Rectangle, Ellipse
from matplotlib.animation import FuncAnimation
import networkx as nx
import matplotlib.pyplot as plt


#BRAIN = None

def set_base_lobe_id(id):
    global BASE_LOBE_ID 
    BASE_LOBE_ID = id
    
def get_base_lobe_id():
    global BASE_LOBE_ID 
    return BASE_LOBE_ID 

def initialize_brain():
    global BRAIN
    BRAIN = Brain()

def get_brain():
    global BRAIN
    if not BRAIN:
        initialize_brain()
    return BRAIN

def get_lobes():
    brain = get_brain()
    return brain.lobes

def get_brain_id():
    brain = get_brain()
    return brain.id

def get_base_lobe():
    brain = get_brain()
    return brain.lobes[brain.base_lobe_id]

def get_base_lobe_id():
    base_lobe = get_base_lobe()
    return base_lobe.id


class Neuron:
    def __init__(self, brain_id, lobe_id, name):
        self.brain_id = brain_id
        self.lobe_id = lobe_id
        self.id = uuid4()
        self.name = name
        self.connections = {
            "from": {},
            "to": {}
        }
        
    def add_connection(self, direction, neuron_id):
        assert direction in ["from", "to"], "Invalid Connection Direction"
        if neuron_id not in self.connections[direction]:
            self.connections[direction][neuron_id] = 1
        else:
            self.connections[direction] += 1
        
        
class Lobe:
    def __init__(self, name, brain_id):
        self.id = uuid4()
        self.name = name
        self.brain_id = brain_id
        self.neurons: Dict[UUID, Neuron] = {}
        self.neuron_idx: Dict[str, UUID] = {}
    
    def neuron_exists(self, identifier):
        if isinstance(identifier, str):
            return bool(identifier in self.neuron_idx and self.neuron_idx[identifier] in self.neurons)
        elif isinstance(identifier, UUID):
            return bool(identifier in self.neurons)
    
    def get_neuron(self, identifier):
        if isinstance(identifier, str):
            id = self.neuron_idx[identifier]
            return self.neurons[id]
        elif isinstance(identifier, UUID):
            return self.neurons[id]
     
    def fetch_neuron(self, identifier):
        if self.neuron_exists(identifier):
            return self.get_neuron[identifier]
        else:
            return self._new_neuron(identifier)
    
    def _new_neuron(self, name):
        neuron = Neuron(self.brain_id, self.id, name)
        self.neurons[neuron.id] = neuron
        self.neuron_idx[name] = neuron.id
        return neuron
        
class Brain:
    def __init__(self):
        self.id = uuid4()
        self.base_lobe_id: UUID = None
        self.lobes: Dict[UUID, Lobe] = {}
        self.lobe_idx: Dict[str, UUID] = {}
        self.neuron_lobe_idx: Dict[UUID, UUID] = {}
        self.fetch_lobe()
        
    def lobe_exists(self, identifier):
        if isinstance(identifier, str):
            return bool(identifier in self.lobe_idx and self.lobe_idx[identifier] in self.lobes)
        elif isinstance(identifier, UUID):
            return bool(identifier in self.lobes)
        
    def get_lobe(self, identifier):
        if isinstance(identifier, str):
            id = self.lobe_idx[identifier]
            return self.lobes[id]
        elif isinstance(identifier, UUID):
            return self.lobes[identifier]
    
    def _new_lobe(self, name):
        lobe = Lobe(name, self.id)
        self.lobes[lobe.id] = lobe
        self.lobe_idx[name] = lobe.id
        if name == "base":
            self.base_lobe_id = lobe.id
            return
        return lobe
    
    def fetch_lobe(self, identifier=None):
        identifier = identifier if identifier is not None else "base"
        if self.lobe_exists(identifier):
            return self.get_lobe(identifier)
        else:
            return self._new_lobe(identifier)
    
    def fetch_neuron_by_name(self, lobe, name):
        neuron = lobe.fetch_neuron(name)
        self.index_neurons([neuron])
        return neuron
    
    def fetch_lobe_by_neuron_id(self, neuron_id) -> Lobe:
        if neuron_id not in self.neuron_lobe_idx:
            return None
        lobe_id = self.neuron_lobe_idx[neuron_id]
        return self.lobes[lobe_id]
        
    
    def index_neurons(self, neurons):
        for neuron in neurons:
            if neuron.id not in self.neuron_lobe_idx:
                self.neuron_lobe_idx[neuron.id] = neuron.lobe_id
    
    def add_synapse(self, from_neuron: Neuron, to_neuron: Neuron):
        self.index_neurons([from_neuron, to_neuron])
        from_neuron.add_connection("to", to_neuron)
        to_neuron.add_connection("from", from_neuron)
        
    def get_brain_map_data(self):
        sections = {}
        connections = []
        for lobe_id in self.lobes:
            lobe: Lobe = self.lobes[lobe_id]
            if lobe.name not in sections:
                sections[lobe.name] = []
            section_items = set(sections[lobe.name])
            for neuron in lobe.neurons.values():
                neuron: Neuron
                section_items.add(neuron.name)
                for direction in ["to", "from"]:
                    for connecting_neuron_id, count in neuron.connections[direction].items():
                        connecting_lobe = self.fetch_lobe_by_neuron_id(connecting_neuron_id)
                        connecting_neuron = connecting_lobe.get_neuron(connecting_neuron_id)
                        for i in range(count):
                            connections.append((
                                neuron.name if direction == "from" else connecting_neuron.name,
                                neuron.name if direction == "to" else connecting_neuron.name
                            ))
            sections[lobe.name] = list(section_items)
        return sections, connections
        
        
    def draw_brain(self):
        sections, connections = self.get_brain_map_data()
        G = nx.DiGraph()
        for lobe, neurons in sections.items():
            for neuron in neurons:
                G.add_node(neuron, section=lobe)
        # Add weighted edges
        for edge in connections:
            if G.has_edge(*edge):
                G[edge[0]][edge[1]]['weight'] += 1  # Increment weight for repeated connection
            else:
                G.add_edge(*edge, weight=1)
                
        # Draw the graph with edge thickness proportional to weight
        pos = nx.spring_layout(G)  # Positioning the nodes
        weights = [G[u][v]['weight'] for u, v in G.edges()]  # Get weights for all edges

        # Draw the nodes and edges
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', width=weights)

        # Show the graph
        plt.show()
    

global interval, frame_pos, total_time
interval = 0
frame_pos = 0
total_time = 0.0

def draw_file(file_path="data.json"):
    brain = json.load(open(file_path, "r"))
    section_colors = {
        "base": "skyblue",
        "Controller": "lightgreen",
        "DeviceStore": "lightcoral",
        "Runner": "orange",
        "_Config": "lightpink",
        "ConfigBuilder": "lightyellow"
    }
    total_frames = len(brain['connections'])
    print(total_frames)
    
    G = nx.DiGraph()
    # Add nodes for sections (they will be square)
    for section in brain['sections']:
        G.add_node(section, shape='square')

    # Add nodes for functions (they will be oval/ellipses)
    for section, functions in brain['sections'].items():
        for function in functions:
            G.add_node(function, shape='oval', section=section, )
            G.add_edge(section, function)
        
    # Add edges based on connections
    for conn in brain['connections']:
        source, target, start_time, end_time, processing_time = conn
        # Count connections between nodes to calculate weight
        if G.has_edge(source, target):
            G[source][target]['weight'] += 1
        else:
            G.add_edge(source, target, weight=1)
    
    # Define a layout (spring layout pulls connected nodes closer)
    pos = nx.spring_layout(G, weight='weight', k=0.5, iterations=50) 

    # Drawing helper for custom shapes
    def draw_nodes_with_shapes(ax, G, pos):
        for node, (x, y) in pos.items():
            if G.nodes[node]['shape'] == 'square':
                ax.add_patch(Rectangle((x - 0.05, y - 0.05), 0.1, 0.1, fill=True, color='lightblue', zorder=2))
                ax.text(x, y, node, fontsize=10, ha='center', va='center', zorder=3)
            else:  # Oval for functions
                ax.add_patch(Ellipse((x, y), 0.15, 0.08, fill=True, color='lightgreen', zorder=2))
                ax.text(x, y, node, fontsize=8, ha='center', va='center', zorder=3)

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Draw nodes and edges in the initial frame
    draw_nodes_with_shapes(ax, G, pos)
    
    for conn in brain["connections"]:
        conn[2] = datetime.strptime(conn[2], "%Y-%m-%d %H:%M:%S.%f")  # Start time
        conn[3] = datetime.strptime(conn[3], "%Y-%m-%d %H:%M:%S.%f")  # End time
    
    # Draw edges (use weights to adjust line width)
    edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", width=[G[u][v]['weight'] for u, v in G.edges], alpha=0.6)
    # Animation update function (here we redraw for every frame if necessary)
    
    def get_next_frame(frame):
        global interval, frame_pos, total_time
        pct = f'{int((frame_pos / len(brain["connections"])) * 100) }%'
        if len(brain["connections"]) -1 > frame_pos:
            frame_pos += 1
        else:
           pct = '100%'
        
        ax.clear()
        source = brain["connections"][frame_pos][0]
        target = brain["connections"][frame_pos][1]
        interval = brain["connections"][frame_pos][4]
        total_time = interval
        title = f"""
        Elapsed: {total_time} seconds
        {pct} Complete
        Caller: {source}
        Target: {target}
        """
        ax.set_title(title, fontsize=14, loc="left")
        
        
        draw_nodes_with_shapes(ax, G, pos)
        # Redraw edges with proper widths
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", width=[G[u][v]['weight'] for u, v in G.edges], alpha=0.5)
        
        edge_width = 2 + interval
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(source, target)], edge_color="red", width=edge_width)
 
    
    print(total_frames)
    global interval
    ani = FuncAnimation(fig, get_next_frame, frames=total_frames, interval=interval, repeat=False)
    plt.show()

draw_file()