
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