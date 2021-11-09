
#import networkx as nx
from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx
import matplotlib.pyplot as plt

n = 6
p = 0.5
#g = nx.generators.random_graphs.random_regular_graph(n, p)
g = erdos_renyi_graph(n, p)
pos = nx.spring_layout(g)
node1=0
node2=1
i=0
path_edges=list(zip([node1],[node2]))

print(g.nodes)
print(g.edges)

nx.draw(g,pos,with_labels = True)
nx.draw_networkx_edges(g,pos,edgelist=path_edges,edge_color='r')
plt.savefig("video_graph"+str(i)+ ".png")
i=1
node1=2
node2=3

path_edges=list(zip([node1],[node2]))
nx.draw_networkx_edges(g,pos,edgelist=path_edges,edge_color='r')
plt.savefig("video_graph"+str(i)+ ".png")