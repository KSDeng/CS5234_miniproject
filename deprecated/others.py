import networkx as nx


def generate_fixed_graph():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_edges_from([(0, 3), (0, 5), (1, 2), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])
    return G

def generate_debug_graph():
    G = nx.Graph()
    G.add_nodes_from([0,1,2,3,4,5,6,7,8,9])
    G.add_edges_from([(0,1),(1,2),(1,5),(2,6),(2,3),(3,7),(3,4),(4,8),(4,9)])
    return G