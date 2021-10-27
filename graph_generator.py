
#import networkx as nx
from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx
import matplotlib.pyplot as plt

n = 100
p = 0.05
#g = nx.generators.random_graphs.random_regular_graph(n, p)
g = erdos_renyi_graph(n, p)

print(g.nodes)
# [0, 1, 2, 3, 4, 5]

print(g.edges)
# [(0, 1), (0, 2), (0, 4), (1, 2), (1, 5), (3, 4), (4, 5)]


nx.draw(g, with_labels = True)
plt.savefig("filename.png")