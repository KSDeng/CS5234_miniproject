"""
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
"""


import networkx as nx
import pylab
from matplotlib import pyplot as plt

def generate_fixed_graph():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_edges_from([(0, 3), (0, 5), (1, 2), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])
    return G

G = generate_fixed_graph()
# 比较美观的可视化参数
plt.figure(figsize=(5,3))
# pos = nx.spring_layout(G, k=1)

# 固定点的位置参数
pos = {0: [0.93976803, 0.53330404],
       1: [-0.27739943, -0.68651481],
       2: [-0.31284206,  0.0360377 ],
       3: [0.21028412, 0.84989332],
       4: [-1.       , -0.5206796],
       5: [ 0.44018934, -0.21204066]}
print(pos)
nx.draw(G, pos, with_labels=True, width=0.4, node_color='lightblue', node_size=400)
# nx.draw(G, pos, with_labels=True, width=0.4, node_color='red', node_size=400)

# highlight source node
#nx.draw(G.subgraph([0]), pos={0:[0.93976803, 0.53330404]}, node_color='red',with_labels=True, width=0.4, node_size=400)

#pos2 = {3:pos[3], 5:pos[5]}
#nx.draw(G.subgraph([3,5]), pos=pos2, node_color='yellow', with_labels=True, width=0.4, node_size=400)
#pos3 = {1:pos[1], 2:pos[2], 4:pos[4]}
#nx.draw(G.subgraph([1,2,4]), pos=pos3, node_color='yellow', with_labels=True, width=0.4, node_size=400)

# highlight edges
nx.draw_networkx_edges(G, pos=pos, edgelist=[(3,2)], edge_color='red')
nx.draw_networkx_edges(G, pos=pos, edgelist=[(2,4)], edge_color='blue')



pylab.show()





