class Node:

    def __init__(self, name: str, sector: str):
        self.name = name
        self.sector = sector
        self.adj_vertices = list()  # list of nodes reference
        self.affinity_hash = dict()  # key = node reference, value = affinity to that node
