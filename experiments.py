from ap_bfs import *
from naive_bfs import *
from matplotlib import pyplot as plt
import random
import time

timestamp = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
print(timestamp)

#N_LIST = [20, 50, 100]
#P_LIST = [0.5, 0.25, 0.1]
N_LIST = [20, 50, 100, 250, 500, 1000]
P_LIST = [0.05]
#P_LIST = [0.5, 0.25, 0.1, 0.01,0.001, 0.0001]

# Experiments 1: test the influence of graph density on naive and ap-bfs algorithm
AP_IO_LIST = []
N_IO_LIST = []
for p in P_LIST:
    for n in N_LIST:
        G = generate_random_graph(n, p)
        # drawGraph(G)
        _, IO_COUNT = AP_BFS(G, 0)
        print('IO_COUNT for AP_BFS: ', IO_COUNT)
        AP_IO_LIST.append(IO_COUNT)
        _, IO_COUNT = N_BFS(G, 0)
        print('IO_COUNT for N_BFS: ', IO_COUNT)
        N_IO_LIST.append(IO_COUNT)

    # draw results
    plt.title("I/Os of naive algorithm and AP-BFS (p ={p})".format(p=p))
    plt.xlabel("n")
    plt.ylabel("I/Os")
    plt.plot(N_LIST, AP_IO_LIST, marker='o', label="AP_BFS")
    plt.plot(N_LIST, N_IO_LIST, marker='o', label="N_BFS")
    plt.legend()
    plt.savefig("graph-{p}-{timestamp}.png".format(p=p, timestamp=timestamp))
    plt.cla()
    AP_IO_LIST = []
    N_IO_LIST = []

# Experiments 2: test the influence of source node selection on ap-bfs algorithm
AP_IO_LIST2 = []
G = generate_random_graph(100, 0.1)
for i in range(100):
    randIndex = random.randint(0, len(G.nodes)-1)
    source = list(G.nodes)[randIndex]
    _, IO_COUNT = AP_BFS(G, source)
    AP_IO_LIST2.append(IO_COUNT)

plt.title("I/O times of AP-BFS at different sources (n = 100, p = 0.1)")
plt.xlabel("Experiments")
plt.ylabel("I/Os")
plt.ylim(0, 500)
plt.plot(range(100), AP_IO_LIST2,marker = 'o')
plt.legend()
plt.savefig("source-result-{timestamp}.png".format(timestamp=timestamp))
plt.cla()
