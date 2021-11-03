from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx
import matplotlib.pyplot as plt

node = 10
p = 0.5

g = erdos_renyi_graph(node, p)
#g = nx.path_graph(6)
pos = nx.spring_layout(g)

#print(g.nodes)
#print(g.edges)
i=0
nx.draw(g,pos,with_labels = True)
source_node=0


def generate_adjlist_with_all_edges(G, delimiter=' '): #https://stackoverflow.com/questions/64433244/generating-adjacency-list-in-networkx-how-to-include-previous-nodes
    for s, nbrs in G.adjacency():
        line = str(s) + delimiter
        for t, data in nbrs.items():
                line += str(t) + delimiter
        yield line[: -len(delimiter)]
        
n=dict()#N(v) denote the set of vertices adjacent to vertex v
 
for line in generate_adjlist_with_all_edges(g):
    adj_list=list(int(i) for i in line.split())
    n[adj_list[0]]=adj_list[1:]
    
print(n)    
def mr_bfs(g,V, s):
    L=dict()#L(i) denote the set of nodes in BFS level i
    N=dict()#N(S) denote the multiset formed by concatenating N(v) for all v in S.
    L[-1]=[]
    L[0]=[s]
    L_p=dict()
    #print(L[0])
    for i in range(1,V):
        
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

    print(L)
mr_bfs(g,node,source_node)




plt.savefig("bfs_graph"+str(i)+ ".png")








