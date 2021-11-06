import networkx as nx
import pylab
from matplotlib import pyplot as plt

# 生成图的参数
n = 6           # 点的个数
p = 0.5         # 点与点间连接的概率

def generate_graph():
    return nx.gnp_random_graph(n=n, p=p)

# TODO
def MR_BFS(G, source):
    return 0

# TODO
def INC_BFS(G, srouce):
    return 0

G = generate_graph()

# 当不是连通图时重新生成
while nx.algorithms.number_connected_components(G) > 1:
    G = generate_graph()

# 比较美观的可视化参数
plt.figure(figsize=(5,3))
pos = nx.spring_layout(G, k=1)
nx.draw(G, pos, with_labels=True, width=0.4, node_color='lightblue', node_size=400)

tree = nx.algorithms.traversal.dfs_tree(G, source=0)       # 用dfs找生成树
nx.draw_networkx_edges(G, pos=pos, edgelist=tree.edges(), edge_color='r')       # 将找到的生成树的边在图上用红色描出来

# 用dfs找生成树的欧拉途径，返回各点的出现次序
euler_tour = list(nx.algorithms.traversal.dfs_preorder_nodes(tree, source=0))
print(euler_tour)

# 对第一个点应用MR_BFS
mr_bfs_res = MR_BFS(G, euler_tour[0])

# 对后续点应用INC_BFS
for i in range(len(euler_tour)):
    if i != 1:
        incremental_bfs_res = INC_BFS(G, euler_tour[i])


pylab.show()            # 展示图




