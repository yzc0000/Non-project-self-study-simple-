#link gitmis
from collections import defaultdict, Counter
from urllib.request import urlopen
import sys
sys.setrecursionlimit(10**7)

class Graph:
    def __init__(self):
        self.adj_list = defaultdict(list)

    def add_edge(self, src, dst):
        self.adj_list[src].append(dst)

    def get_nodes(self):
        nodes = set(self.adj_list.keys())
        for neighbors in self.adj_list.values():
            nodes.update(neighbors)
        return list(nodes)

    def reverse(self):
        reversed_g = Graph()
        for src in self.adj_list:
            for dst in self.adj_list[src]:
                reversed_g.add_edge(dst, src)
        return reversed_g

def dfs(graph, node, visited, leader, s, finishing_time, t):
    visited.add(node)
    leader[node] = s
    for neighbor in graph.adj_list[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, leader, s, finishing_time, t)
    t[0] += 1
    finishing_time[node] = t[0]

def dfs_loop(graph, nodes, finishing_time=None):
    visited = set()
    leader = {}
    t = [0]
    for node in nodes:
        if node not in visited:
            s = node
            dfs(graph, node, visited, leader, s, finishing_time if finishing_time is not None else {}, t)
    return leader, finishing_time

def kosaraju_scc(graph):
    reversed_graph = graph.reverse()
    nodes = reversed_graph.get_nodes()
    nodes.sort(reverse=True)

    finishing_time = {}
    leader, finishing_time = dfs_loop(reversed_graph, nodes, finishing_time)

    ordered_nodes = sorted(finishing_time, key=finishing_time.get, reverse=True)

    leader, _ = dfs_loop(graph, ordered_nodes)

    return Counter(leader.values())

def read_graph_from_url(url):
    graph = Graph()
    with urlopen(url) as f:
        for line in f:
            line = line.decode().strip()
            if line == "":
                continue
            src, dst = map(int, line.split())
            graph.add_edge(src, dst)
    return graph


url = "https://d3c33hcgiwev3.cloudfront.net/_410e934e6553ac56409b2cb7096a44aa_SCC.txt?Expires=1753833600&Signature=PZQhJl0eW4yMYLfYlUZoSWTROG7SmilU6nj9PP6nU8oKHVss9VhlPIuTjYR3m1pRS3OFkFDAlBAraYLkxHeEfyrtZ2D-WbgqRdbHGa-sDn9UIB4d6xkxuBgaBdn5zE4YEnybbEMZ4dYNmTVxQPDS7MjiSdCrgn4-t45Y7AL9Qx4_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"

graph = read_graph_from_url(url)

scc_sizes = kosaraju_scc(graph)
sizes = sorted(scc_sizes.values(), reverse=True)
top5 = sizes[:5] + [0]*(5 - len(sizes))
output = ",".join(map(str, top5))
print(output)
