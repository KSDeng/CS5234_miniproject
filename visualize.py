import networkx as nx
from pylab import *

# generate and draw graph
subplot(1,2,1)
nx.draw(nx.gnm_random_graph(10,20))
title('random graph with 10 nodes, 20 edges')

subplot(1,2,2)
nx.draw(nx.gnp_random_graph(30,0.05))
title('random graph with 20 nodes, 0.1 edge probability')

show()

# make graph visualization more readable
from matplotlib import pyplot as plt

G = nx.fast_gnp_random_graph(100,.05)
plt.figure(figsize=(10,6))
pos = nx.spring_layout(G, k=0.8)
nx.draw(G, pos, with_labels=True, width=0.4, node_color='lightblue', node_size=400)
show()