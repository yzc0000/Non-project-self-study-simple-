import heapq

def read_graph(filename):
    graph = {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            node = int(parts[0])
            edges = []
            for edge_info in parts[1:]:
                if edge_info:
                    neighbor, weight = edge_info.split(',')
                    edges.append((int(neighbor), int(weight)))
            graph[node] = edges
    return graph

def dijkstra(graph, source, n):
    dist = [10**6] * (n + 1)
    dist[source] = 0
    heap = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > dist[u]:
            continue
        for v, w in graph.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist

if __name__ == "__main__":
    filename = "djikstradata"  # Dosya adı
    n = 200
    graph = read_graph(filename)
    dist = dijkstra(graph, 1, n)

    targets = [7,37,59,82,99,115,133,165,188,197]
    result = ",".join(str(dist[v]) if dist[v] != 10**6 else "1000000" for v in targets)
    print(result)
