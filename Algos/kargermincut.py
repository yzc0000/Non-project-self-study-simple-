def karger_min_cut(graph):
    import random
    import copy

    local_graph = copy.deepcopy(graph)

    while len(local_graph) > 2:
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

    remaining_nodes = list(local_graph.keys())
    cut_size = len(local_graph[remaining_nodes[0]])
    return cut_size


def read_graph_from_file(filename):
    graph = {}
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            node = parts[0]
            neighbors = parts[1:]
            graph[node] = neighbors
    return graph

filename = "mincut Adjacency list data"
graph = read_graph_from_file(filename)

min_cut = float('inf')
for i in range(100):
    result = karger_min_cut(graph)
    if result < min_cut:
        min_cut = result

print("Minimum Cut:", min_cut)
