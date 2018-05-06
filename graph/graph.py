class Graph:

    def __init__(self):
        self.adjacency_list = list()  # list of node references
        self.obj_map = dict()  # key = node reference, value = index of that node reference in adjacency_list
        self.name_map = dict()  # key = node name, value = index of that node reference in adjacency_list

    def set_name_obj_map(self):
        for i in range(len(self.adjacency_list)):
            self.obj_map[self.adjacency_list[i]] = i
            self.name_map[self.adjacency_list[i].name] = i

    def greatest_edge(self) -> float:
        maximum = 0.0
        for actual_node in self.adjacency_list:
            for node in actual_node.adj_vertices:
                affinity = actual_node.affinity_hash[node]
                if affinity > maximum:
                    maximum = affinity
        return maximum
