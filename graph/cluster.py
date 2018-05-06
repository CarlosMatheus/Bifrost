
class Element:

    def __init__(self, node):
        self.node = node

    def dist(self, other: 'Element'):
        pass


class Cluster:

    def __init__(self):
        self.size = 0
        self.elements = []
        self.centroid = None

    def dist(self, other: 'Cluster') -> float:
        pass


class Clusterization:

    def __init__(self, graph):
        self.size = graph.num_nodes
        self.elements = []
        self.clusters = []
        self.dist_matrix = []

