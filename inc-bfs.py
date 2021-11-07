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
    return L


# 测试差集

# list1 = [1,2,3,4,5]
# list2 = [3,4,5,6,7]
# r1 = [item for item in list1 if item not in list2]
# print(r1)

G = generate_fixed_graph()
adj_list = generate_adjlist_as_dict(G)
print(adj_list)
dist0 = {1:2, 2:2, 3:1, 4:3, 5:1}       # generate by MR-BFS


L1 = INC_BFS(G, 0, 3, dist0, adj_list)

# sort ajd_list according to dist0
print(dist0)
sorted_adj_list = sort_adj_list_by_dist(adj_list, dist0)
print(sorted_adj_list)

# test MR-BFS
L = MR_BFS(G, 0, adj_list)

portion_adj_list = get_portion_of_sorted_adj_list(dist0, sorted_adj_list, 2)
print(portion_adj_list)

print(len(G.nodes))