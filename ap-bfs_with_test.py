import math
import networkx as nx
import pylab
from matplotlib import pyplot as plt
import time
import random
from itertools import combinations, groupby

M = 5120000         # Memory size
B = 512             # Block size of disk
IO_COUNT = 0

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

def generate_random_graph(n, p):
    G = nx.erdos_renyi_graph(n, p)
    if nx.is_connected(G):
        return G
    else:
        components = dict(enumerate(nx.connected_components(G)))
        components_combs = combinations(components.keys(), r=2)
        
        for _, node_edges in groupby(components_combs, key=lambda x: x[0]):
            node_edges = list(node_edges)
            random_comps = random.choice(node_edges)
            source = random.choice(list(components[random_comps[0]]))
            target = random.choice(list(components[random_comps[1]]))
            G.add_edge(source, target)
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


def get_source_node_max_neighbor(G):
    res=dict()
    for node in list(G.nodes):
        res[node]=len(list(G.neighbors(node)))
    #print(res)
    sn = max(res, key=lambda x: res[x])
    return sn

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


def test_adj(G):
    n=dict()
    for line in nx.generate_adjlist(G):
        adj_list=list(int(i) for i in line.split())
        n[adj_list[0]]=adj_list[1:]
    return n

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

def MR_BFS(G, source, adj_list):
    L = {-1:[], 0:[source]}         # ???????????????
    for i in range(1, len(G.nodes)):

        # Step (1): Construct N(L(i-1)) by accessing the adjacency list of nodes in L(i-1)
        temp = []
        for node in L[i-1]:
            temp += adj_list[node]

        # Step (2): Remove the duplicates in N[i-1] by sorting the nodes in N[i-1] by node indexes
        temp.sort()
        temp = list(set(temp))
        # the result is L'(i)

        # Step (3): Remove the nodes appear in L(i-1) and L(i-2)
        temp = [item for item in temp if item not in L[i-1]]
        temp = [item for item in temp if item not in L[i-2]]
        L[i] = temp

    # I/O complexity: O(V + sort(E))
    # sort(E) = O(E/B log(E/B, base = M/B))
    global IO_COUNT
    E = float(len(G.edges))
    sortE_IO = max(math.ceil(math.ceil(E/B) * math.log(math.ceil(E/B), math.floor(M/B))), 1)
    IO_COUNT += (len(G.nodes) + sortE_IO)
    return L

def INC_BFS(G, U, V, dist, adj_list):
    L = {-1:[], 0:[V]}

    sorted_adj_list = sort_adj_list_by_dist(adj_list, dist)

    for i in range(1, len(G.nodes)):

        # Step (1): Extract the adjacency list of each w E V[G] that appears in
        # L(i - 1) and whose adjacency list appears in A(j) by scanning L(i - 1) and A(j) simultaneously.
        temp = []
        for j in range(max(0, i-1-dist[V]), min(len(G.nodes)-1, i-1+dist[V])+1):
            
            Ai = get_portion_of_sorted_adj_list(dist, sorted_adj_list, j)
            for node in L[i-1]:
                if node in Ai.keys():
                    temp += Ai[node]

        # Step (2): Remove the duplicates in N[i-1] by sorting the nodes in N[i-1] by node indexes
        temp.sort()
        temp = list(set(temp))
        # the result is L'(i)

        # Step (3): Remove the nodes appear in L(i-1) and L(i-2)
        temp = [item for item in temp if item not in L[i-1]]
        temp = [item for item in temp if item not in L[i-2]]
        L[i] = temp

    # I/O complexity: O(E/B*d(u,v) + sort(E))
    global IO_COUNT
    E = float(len(G.edges))

    #sortE_IO = max(math.ceil(math.ceil(E/B) * math.log(math.ceil(E/B), math.floor(M/B))), 1)
    #IO_COUNT += math.ceil(math.ceil(E/B)*dist[V] + sortE_IO)

    # debug
    IO_COUNT += math.ceil(math.ceil(E/B)*dist[V])

    return L

# debug
AP_BFS_IO_ARRAY = []
N_BFS_IO_ARRAY = []

def AP_BFS(G, source):
    APSP_RES = {}           # APSP???????????????????????????????????????
    adj_list = generate_adj_list_as_dict(G)
    global IO_COUNT

    # Step (1) a: Find a spanning tree T of G
    tree = nx.algorithms.traversal.dfs_tree(G, source=source)  # ??????fs??????????????????

    # I/O complexity: O(min{V+sort(E), sort(E)*log(log(V,base=2),base=2)})
    V, E = float(len(G.nodes)), float(len(G.edges))
    sortE_IO = max(math.ceil(math.ceil(E/B)*math.log(math.ceil(E/B), math.floor(M/B))),1)
    p1 = math.ceil(V + sortE_IO)
    p2 = math.ceil(sortE_IO * math.log(math.log(V, 2), 2))
    IO_COUNT += min(p1, p2)

    # Step (1) b and c: Construct a Euler Tour ET for T
    # and mark the first occurrence of each vertex on ET
    euler_tour = list(nx.algorithms.traversal.dfs_preorder_nodes(tree, source=source))  # ??????fs???????????????????????????????????????????????????????????????????????????????????????

    # I/O complexity: O(sort(V)) + O(sort(E))
    sortV_IO = max(math.ceil(math.ceil(V/B) * math.log(math.ceil(V/B), math.floor(M/B))), 1)
    IO_COUNT += (sortV_IO + sortE_IO)

    # Step (2): Run MR-BFS with the first node in the occurrence
    level_dict0 = MR_BFS(G, source, adj_list)
    dist_dict0 = get_dist_from_level(level_dict0)

    # debug
    AP_BFS_IO_ARRAY.append(IO_COUNT)

    dist_dict0 = dict(sorted(dist_dict0.items(), key=lambda item:item[0]))
    APSP_RES[source] = dist_dict0

    # Step (3): Run Incremental-BFS for the remaining nodes in the occurrence
    for i in range(1, len(euler_tour)):
        last_io_count = IO_COUNT
        incremental_bfs_res = INC_BFS(G, euler_tour[i-1], euler_tour[i], APSP_RES[euler_tour[i-1]], adj_list)
        dist_dict = get_dist_from_level(incremental_bfs_res)
        dist_dict = dict(sorted(dist_dict.items(), key=lambda item:item[0]))
        APSP_RES[euler_tour[i]] = dist_dict

        # debug
        AP_BFS_IO_ARRAY.append(IO_COUNT - last_io_count)

    return APSP_RES


def N_BFS(G, source):
    N_RES = {}
    adj_list = generate_adj_list_as_dict(G)

    # Step (2): Run MR-BFS with the all node.
    for node in G.nodes:
        last_io_count = IO_COUNT
        level_dict0 = MR_BFS(G, node, adj_list)
        dist_dict0 = get_dist_from_level(level_dict0)

        N_RES[node] = dist_dict0

        # debug
        N_BFS_IO_ARRAY.append(IO_COUNT - last_io_count)

    """ 
    for i in range(len(G.nodes())):
        last_io_count = IO_COUNT
        level_dict0 = MR_BFS(G, i, adj_list)
        dist_dict0 = get_dist_from_level(level_dict0)
    
        N_RES[i] = dist_dict0

        # debug
        N_BFS_IO_ARRAY.append(IO_COUNT - last_io_count)
    """

    return N_RES

def drawGraph(G):
    pos = nx.spring_layout(G, k=1)
    nx.draw(G, pos, with_labels=True, width=0.4, node_color='lightblue', node_size=400)
    pylab.show()

#IO count 
#N_LIST = [20, 50, 100, 250, 500, 1000]
#P_LIST = [0.5, 0.25, 0.1, 0.01,0.001, 0.0001]
N_LIST = [80]
P_LIST = [0.5]

#tests
def naive_test():
    global IO_COUNT
    AP_IO_LIST = []
    N_IO_LIST = []
    for p in P_LIST:
        for n in N_LIST:
            G = generate_random_graph(n,p)
            drawGraph(G)
            IO_COUNT = 0
            res_ap = AP_BFS(G, 0)
            print('IO_COUNT for AP_BFS: ', IO_COUNT)
            AP_IO_LIST.append(IO_COUNT)
            
            IO_COUNT = 0
            res_n = N_BFS(G, 0)
            print('IO_COUNT for N_BFS: ', IO_COUNT)
            N_IO_LIST.append(IO_COUNT)

        """
        plt.title("p = "+ str(p)) 
        plt.xlabel("n")
        plt.ylabel("I/Os")
        plt.plot(N_LIST, AP_IO_LIST,marker = 'o', label = "AP_BFS")
        plt.plot(N_LIST, N_IO_LIST,marker = 'o', label = "N_BFS")
        plt.legend()
        plt.savefig("graph" + str(p) + ".png")
        plt.cla()
        AP_IO_LIST = []
        N_IO_LIST = []
        """
        
def source_node_test():
    global IO_COUNT
    AP_IO_LIST = []
    APMH_IO_LIST = []
    for p in P_LIST:
        for n in N_LIST:
            #source_node = 0
            G = generate_random_graph(n, p)
            IO_COUNT = 0
            res_ap = AP_BFS(G, 0)
            AP_IO_LIST.append(IO_COUNT)
            
            #source_node = max_neighbors
            sn = get_source_node_max_neighbor(G)
            IO_COUNT = 0
            res_n = AP_BFS(G, sn)
            APMH_IO_LIST.append(IO_COUNT)
        
        plt.title("p = "+ str(p)) 
        plt.xlabel("n")
        plt.ylabel("I/Os")
        plt.plot(N_LIST, AP_IO_LIST,marker = 'o', label = "AP_BFS source node = 0")
        plt.plot(N_LIST, APMH_IO_LIST,marker = 'o', label = "AP_BFS source node = max_neighbors")
        plt.legend()
        plt.savefig("node_graph" + str(p) + ".png")
        plt.cla()
        AP_IO_LIST = []
        APMH_IO_LIST = []
        






#G = generate_fixed_graph()
#res = AP_BFS(G, 0)
#print(res)
#print(IO_COUNT)

naive_test()

# debug
#G = generate_debug_graph()
# G = generate_fixed_graph()
# pos = nx.spring_layout(G, k=1)
'''
pos = {0: [-0.87683555,  0.36644588],
1: [-0.50426159, -0.33825496], 2: [ 0.17216437, -0.10865578],
 3: [-0.18483911,  0.27282255], 4: [0.47763095, 0.30200949],
 5: [-0.41047382, -1.        ], 6: [0.94495623, 0.02538161],
 7: [-0.87848839,  0.08289201], 8: [0.73522478, 0.89431526],
 9: [ 0.52492213, -0.49695606]}
'''
"""
pos = {0: [0.93976803, 0.53330404],
       1: [-0.27739943, -0.68651481],
       2: [-0.31284206,  0.0360377 ],
       3: [0.21028412, 0.84989332],
       4: [-1.       , -0.5206796],
       5: [ 0.44018934, -0.21204066]}
"""

# print(pos)
#nx.draw(G, pos, with_labels=True, width=0.4, node_color='lightblue', node_size=400)
#pylab.show()
#res = AP_BFS(G, 0)
#res = dict(sorted(res.items(), key=lambda item: item[0]))
'''
for i in range(0,10):
    print('{ii}\t'.format(ii=i))
    values = res[i]
    values = dict(sorted(values.items(), key=lambda item:item[0]))
    print(values)
'''

# print(res)

