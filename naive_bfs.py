import math
from utils import *

M = 5120000         # Memory size
B = 512             # Block size of disk

IO_COUNT = 0

def MR_BFS(G, source, adj_list):
    L = {-1:[], 0:[source]}         # 鍒濆鍖朙
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
    sortE_IO = max(math.ceil(math.ceil(E / B) * math.log(math.ceil(E / B), math.floor(M / B))), 1)
    IO_COUNT += (len(G.nodes) + sortE_IO)
    return L

def N_BFS(G, source):
    N_RES = {}
    adj_list = generate_adj_list_as_dict(G)

    global IO_COUNT
    IO_COUNT = 0

    # Step (2): Run MR-BFS with the all node.
    for node in G.nodes:
        level_dict0 = MR_BFS(G, node, adj_list)
        dist_dict0 = get_dist_from_level(level_dict0)

        N_RES[node] = dist_dict0

    return N_RES, IO_COUNT