import networkx as nx
import pylab
from matplotlib import pyplot as plt

G = nx.path_graph(5)

G = nx.gnm_random_graph(20, 40)
plt.figure(figsize=(5,3))
pos = nx.spring_layout(G, k=1)
nx.draw(G, pos, with_labels=True, width=0.4, node_color='lightblue', node_size=400)


T = nx.algorithms.traversal.dfs_tree(G,0)
print(list(T.edges()))
nx.draw_networkx_edges(G, pos=pos, edgelist=T.edges(),edge_color='r')
pylab.show()

def generate_adjlist_with_all_edges(G, delimiter=' '):
    # https://stackoverflow.com/questions/64433244/generating-adjacency-list-in-networkx-how-to-include-previous-nodes
    for s, nbrs in G.adjacency():
        line = str(s) + delimiter
        for t, data in nbrs.items():
            line += str(t) + delimiter
        yield line[: -len(delimiter)]