current_label = 7
class Graph:
    def __init__(self):
        self.adj_list = {}
        self.topo_order = {}

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, src, dst):
        self.adj_list[src].append(dst)

    def dfs(self):
        visited = set()
        for node in self.adj_list:
            if node not in visited:
                self._dfs_recursive(node, visited)

    def _dfs_recursive(self, node, visited):
        global current_label
        visited.add(node)
        print(node, end=" ")
        for neighbor in self.adj_list[node]:
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited)
        self.topo_order[node] = current_label
        current_label -= 1


    def print_graph(self):
        for node in self.adj_list:
            print(f"{node}: {self.adj_list[node]}")

g = Graph()


for node in ["A", "B", "C", "D", "E", "F", "G"]:
    g.add_node(node)

g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("B", "E")
g.add_edge("C", "D")
g.add_edge("A", "D")
g.add_edge("F", "G")

g.print_graph()

g.dfs()
print("\nTopolojik sıralama (düğüm: label):")
for node, label in g.topo_order.items():
    print(f"{node}: {label}")