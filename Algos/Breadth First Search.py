from collections import deque

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, src, dst):
        self.adj_list[src].append(dst)
        self.adj_list[dst].append(src)

    def bfs(self, start, target):
        visited = set()
        distance = {}
        parent = {}
        found = False

        for i in self.adj_list:
            if i not in visited:
                queue = deque()
                queue.append(i)
                visited.add(i)
                distance[i] = 0
                parent[i] = None

                print(f"BFS from component starting at '{i}':", end=" ")

                while queue:
                    current = queue.popleft()
                    print(current, end=" ")

                    if current == target:
                        found = True
                        print("\nTarget found!")
                        path = []
                        while current is not None:
                            path.append(current)
                            current = parent[current]
                        path.reverse()
                        print("En kısa yol:", " -> ".join(path))
                        print("Mesafe:", distance[path[-1]])
                        return distance[path[-1]]

                    for neighbor in self.adj_list[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                            distance[neighbor] = distance[current] + 1
                            parent[neighbor] = current
                print()

        if not found:
            print(f"\nHedef '{target}' hiçbir bileşende bulunamadı.")



    def print_graph(self):
        for node in self.adj_list:
            print(f"{node}: {self.adj_list[node]}")
g = Graph()

for node in ["A", "B", "C", "D", "E","F","G"]:
    g.add_node(node)

g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("B", "E")
g.add_edge("C", "D")
g.add_edge("A", "D")
g.add_edge("F","G")
g.print_graph()

g.bfs("A", "G")
