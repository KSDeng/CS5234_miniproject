import math
from utils import *

M = 5120000         # Memory size
B = 512             # Block size of disk

IO_COUNT = 0

def MR_BFS(G, source, adj_list):
    L = {-1:[], 0:[source]}         # 初始化L
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
    sortE_IO = max(math.ceil(math.ceil(E/B) * math.log(math.ceil(E/B), math.floor(M/B))), 1)
    IO_COUNT += math.ceil(math.ceil(E/B)*dist[V] + sortE_IO)

    return L

def AP_BFS(G, source):
    APSP_RES = {}           # APSP问题最终求解结果
    adj_list = generate_adj_list_as_dict(G)

    global IO_COUNT
    IO_COUNT = 0

    # Step (1) a: Find a spanning tree T of G
    tree = nx.algorithms.traversal.dfs_tree(G, source=source)  # 用dfs找生成树

    # I/O complexity: O(min{V+sort(E), sort(E)*log(log(V,base=2),base=2)})
    V, E = float(len(G.nodes)), float(len(G.edges))
    sortE_IO = max(math.ceil(math.ceil(E/B)*math.log(math.ceil(E/B), math.floor(M/B))),1)
    p1 = math.ceil(V + sortE_IO)
    p2 = math.ceil(sortE_IO * math.log(math.log(V, 2), 2))
    IO_COUNT += min(p1, p2)

    # Step (1) b and c: Construct a Euler Tour ET for T
    # and mark the first occurrence of each vertex on ET
    euler_tour = list(nx.algorithms.traversal.dfs_preorder_nodes(tree, source=source))  # 用dfs找生成树的欧拉途径，返回各点的出现次序

    # I/O complexity: O(sort(V)) + O(sort(E))
    sortV_IO = max(math.ceil(math.ceil(V/B) * math.log(math.ceil(V/B), math.floor(M/B))), 1)
    IO_COUNT += (sortV_IO + sortE_IO)

    # Step (2): Run MR-BFS with the first node in the occurrence
    level_dict0 = MR_BFS(G, source, adj_list)
    dist_dict0 = get_dist_from_level(level_dict0)

    dist_dict0 = dict(sorted(dist_dict0.items(), key=lambda item:item[0]))
    APSP_RES[source] = dist_dict0

    # Step (3): Run Incremental-BFS for the remaining nodes in the occurrence
    for i in range(1, len(euler_tour)):
        incremental_bfs_res = INC_BFS(G, euler_tour[i-1], euler_tour[i], APSP_RES[euler_tour[i-1]], adj_list)
        dist_dict = get_dist_from_level(incremental_bfs_res)
        dist_dict = dict(sorted(dist_dict.items(), key=lambda item:item[0]))
        APSP_RES[euler_tour[i]] = dist_dict
    return APSP_RES, IO_COUNT



