import math
import networkx as nx

M = 100.0         # Memory size
B = 10.0          # Block size of disk
IO_COUNT = 0

def generate_fixed_graph():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_edges_from([(0, 3), (0, 5), (1, 2), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])
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
        if key <= 0 or not value or len(value) == 0:
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

    APSP_RES[source] = dist_dict0

    # Step (3): Run Incremental-BFS for the remaining nodes in the occurrence
    for i in range(1, len(euler_tour)):
        incremental_bfs_res = INC_BFS(G, euler_tour[i-1], euler_tour[i], dist_dict0, adj_list)
        dist_dict = get_dist_from_level(incremental_bfs_res)
        APSP_RES[euler_tour[i]] = dist_dict
    return APSP_RES


G = generate_fixed_graph()
res = AP_BFS(G, 0)
print(res)
print(IO_COUNT)


