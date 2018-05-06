from graph import Graph
from node import Node


class GraphMaker:

    @classmethod
    def create_graph(cls, pyrebase, people_and_sector_list):
        db = pyrebase.database()
        data_hash_of_hash = cls.__get_data_hash(db)

        graph = cls.__initiate_graph(people_and_sector_list)
        graph.set_name_map()
        cls.__set_all_affinities_to_zero()

        cls.__insert_data(graph, data_hash_of_hash)

    @classmethod
    def __initiate_graph(cls, people_and_sector_list):
        g = Graph()
        for elem in people_and_sector_list:
            name = elem["name"]
            sector = elem["sector"]
            g.adjacency_list.append(Node(name, sector))
        return g

    @classmethod
    def __get_data_hash(cls, db):
        #todo
        # Return the hash with the data
        return 0

    @classmethod
    def __set_all_affinities_to_zero(cls, graph):
        """
        n^2 alg -> set all node adjacent list to all other nodes having affinity zero
        """
        for node in graph.adjacency_list:
            for node_to_add in graph.adjacency_list:
                if node_to_add != node:
                    tup_to_add = (node_to_add, 0)
                    node.adj_vertices.append(tup_to_add)

    @classmethod
    def __insert_data(cls, graph, data_hash_of_hash):
        for key, value in data_hash_of_hash:
            for node in value:
                destiny_node = graph.adjacency_list[graph.name_map[node["destiny"]]]
                actual_graph_node = graph.adjacency_list[graph.name_map[key]]
                if destiny_node not in actual_graph_node:
                    tup_to_add = (destiny_node, 1)
                    actual_graph_node.adjacency_list = tup_to_add

