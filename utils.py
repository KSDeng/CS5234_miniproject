import networkx as nx
import pylab

def generate_random_graph(n, p):
    G = nx.gnp_random_graph(n, p)
    while not nx.is_connected(G):
        G = nx.gnp_random_graph(n, p)
    return G

def generate_adj_list_as_dict(G):
    '''
    :param G: graph
    :return: dict, the adjacency list of G
    '''
    adj_list = {}
    for s, nbrs in G.adjacency():
        adj_list[s] = list(nbrs.keys())
    return adj_list

def get_dist_from_level(level_dict):
    '''
    Transform the level-form dict to dist-form dict
    :param level_dict:
    :return:
    '''
    dist_dict = {}
    for key, value in level_dict.items():
        if key < 0 or not value or len(value) == 0:
            continue
        for node in value:
            dist_dict[node] = key
    return dist_dict

def sort_adj_list_by_dist(adj_list, dist):
    '''
    :param adj_list: adjacency list of a graph G
    :param dist: distances from u to other nodes
    :return: adjacency list of non-descending order by the distance from u
    '''

    dist_sorted = dict(sorted(dist.items(), key=lambda item: item[1]))
    sorted_adj_list = {}
    for key in dist_sorted:
        sorted_adj_list[key] = adj_list[key]
    return sorted_adj_list

def get_portion_of_sorted_adj_list(dist, sorted_adj_list, i):
    '''
    :param dist: distances list of other nodes from u
    :param sorted_adj_list: sorted adjacency list
    :param i: distance from u
    :return: the portion of the sorted adjacency list that contains adjacency lists of vertices
                lying exactly at distance i from u
    '''
    portion_adj_list = {}
    for key, value in sorted_adj_list.items():
        if dist[key] == i:
            portion_adj_list[key] = value
    return portion_adj_list

def get_source_node_max_neighbor(G):
    res=dict()
    for node in list(G.nodes):
        res[node]=len(list(G.neighbors(node)))
    #print(res)
    sn = max(res, key=lambda x: res[x])
    return sn

def drawGraph(G):
    pos = nx.spring_layout(G, k=1)
    nx.draw(G, pos, with_labels=True, width=0.4, node_color='lightblue', node_size=400)
    pylab.show()

