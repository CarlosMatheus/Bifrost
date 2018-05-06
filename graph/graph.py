class Graph:

    def __int__(self):
        self.adjacency_list = list()
        self.name_map = dict()

    @property
    def size(self):
        return len(self.adjacency_list)

    def set_name_map(self):
        for i in range(len(self.adjacency_list)):
            self.name_map[self.adjacency_list[i]] = i

    def greatest_edge(self) -> float:
        maximum = 0.0
        for actual_node in self.adjacency_list:
            for node in actual_node.adj_vertices:
                affinity = actual_node.affinity_hash[node]
                if affinity > maximum:
                    maximum = affinity
        return maximum
