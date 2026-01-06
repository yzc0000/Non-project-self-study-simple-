#Plus Plotting

import random
import copy
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph, step):
    G = nx.MultiGraph()

    # Grafı networkx'e çeviriyoruz
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    plt.figure(figsize=(6, 4))
    pos = nx.spring_layout(G)  # Düğüm pozisyonları
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
    plt.title(f"Graph after contraction step {step}")
    plt.show()


def karger_min_cut(graph):
    local_graph = copy.deepcopy(graph)
    step = 0

    while len(local_graph) > 2:
        step += 1

        u = random.choice(list(local_graph.keys()))
        v = random.choice(local_graph[u])
        super_node = u + v

        local_graph[super_node] = []
        for node in local_graph[u]:
            if node != v:
                local_graph[super_node].append(node)
        for node in local_graph[v]:
            if node != u:
                local_graph[super_node].append(node)

        for node in local_graph:
            if node in [u, v, super_node]:
                continue
            local_graph[node] = [super_node if x in [u, v] else x for x in local_graph[node]]

        local_graph[super_node] = [x for x in local_graph[super_node] if x != super_node]

        del local_graph[u]
        del local_graph[v]

        # Her iteration'dan sonra grafı çizdir
        draw_graph(local_graph, step)

    remaining_nodes = list(local_graph.keys())
    cut_size = len(local_graph[remaining_nodes[0]])
    return cut_size

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'C'],
    'C': ['A', 'D', 'B'],
    'D': ['B', 'C']
}

min_cut = float('inf')
for i in range(1):
    result = karger_min_cut(graph)
    if result < min_cut:
        min_cut = result

print("Minimum Cut:", min_cut)
