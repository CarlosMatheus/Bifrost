class Graph:

    def __int__(self):
        self.adjacency_list = list()
        self.name_map = dict()

    def set_name_map(self):
        for i in range(len(self.adjacency_list)):
            self.name_map[self.adjacency_list[i]] = i
