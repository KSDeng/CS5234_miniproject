from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx
import matplotlib.pyplot as plt
'''
node = 10
p = 0.5

g = erdos_renyi_graph(node, p)
#g = nx.path_graph(6)
pos = nx.spring_layout(g)

#print(g.nodes)
#print(g.edges)
i=0
nx.draw(g,pos,with_labels = True)
'''

def generate_fixed_graph():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_edges_from([(0, 3), (0, 5), (1, 2), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])
    return G

source_node=0

'''
def generate_adjlist_with_all_edges(G, delimiter=' '): #https://stackoverflow.com/questions/64433244/generating-adjacency-list-in-networkx-how-to-include-previous-nodes
    for s, nbrs in G.adjacency():
        line = str(s) + delimiter
        for t, data in nbrs.items():
                line += str(t) + delimiter
        yield line[: -len(delimiter)]
'''     

def generate_adjlist_as_dict(G):
    adj_list = {}
    for s, nbrs in G.adjacency():   
        adj_list[s] = list(nbrs.keys())
    return adj_list
   
def mr_bfs(g, s):
    dist=dict()
    L=dict()#L(i) denote the set of nodes in BFS level i
    N=dict()#N(S) denote the multiset formed by concatenating N(v) for all v in S.
    L[-1]=[]
    L[0]=[s]
    L_p=dict()
    #print(L[0])
    for i in range(1,len(g.nodes)):
        
        #construct N(L(i-1))
        N[i]=[]
        for j in L[i-1]:
            N[i]=N[i]+n[j]
            
        #sort
        N[i].sort()
        #scan and compaction
        N[i]=list(set(N[i]))
        N[i].sort()
        L_p[i]=N[i]
        #print("L_p[i]: ", L_p[i])
        #print("i-1: ",L[i-1])
        #print("i-2: ",L[i-2])
        L[i]=[]
        for nodes in L_p[i]:
            #print("node: ",nodes)
            if nodes not in L[i-1]:
                if nodes not in L[i-2]:                 
                    #print(nodes)
                    L[i].append(nodes)

    
    #print("BFS Level: ", L)
    
    for k,v in L.items():
        if k >=0:
            for i in v:
                dist[i]=k
    return dist
    
    
    

g = generate_fixed_graph()
pos = nx.spring_layout(g, k=1)
nx.draw(g, pos, with_labels=True, width=0.4, node_color='lightblue', node_size=400)

n=generate_adjlist_as_dict(g)#N(v) denote the set of vertices adjacent to vertex v
'''
for line in generate_adjlist_with_all_edges(g):
    adj_list=list(int(i) for i in line.split())
    n[adj_list[0]]=adj_list[1:]
    
print(n) 
'''

#print("graph adj list: ", n)
mr_bfs(g,source_node)



i = 0
plt.savefig("bfs_graph"+str(i)+ ".png")








