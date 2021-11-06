import networkx as nx

# input: G, u, v, d(u,*)
# G: graph
# u: start node
# v: another node of whose distances to other nodes you want to calculate
# d(u, *): a dict describing the distance from u to other nodes

# adj: adjacency list of G

def generate_fixed_graph():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_edges_from([(0, 3), (0, 5), (1, 2), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])
    return G

def generate_adjlist_as_dict(G):
    '''
    :param G: graph
    :return: dict, the adjacency list of G
    '''
    adj_list = {}
    for s, nbrs in G.adjacency():
        adj_list[s] = list(nbrs.keys())
    return adj_list

def sort_adj_list_by_dist(adj_list, dist):
    '''
    :param adj_list: adjacency list of a graph G
    :param dist: distances from u to other nodes
    :return: adjacency list of non-descending order by the distance from u
    '''

    dist_sorted = dict(sorted(dist.items(), key=lambda item:item[1]))
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

G = generate_fixed_graph()
adj_list = generate_adjlist_as_dict(G)
print(adj_list)
dist0 = {1:2, 2:2, 3:1, 4:3, 5:1}       # generate by MR-BFS
# sort ajd_list according to dist0
print(dist0)
sorted_adj_list = sort_adj_list_by_dist(adj_list, dist0)
print(sorted_adj_list)

portion_adj_list = get_portion_of_sorted_adj_list(dist0, sorted_adj_list, 2)
print(portion_adj_list)

print(len(G.nodes))