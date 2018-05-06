from graph.graph import Graph
from graph.node import Node


class GraphMaker:

    @classmethod
    def create_graph(cls, pyrebase, people_and_sector_list):
        db = pyrebase.database()
        data_hash_of_hash = cls.__get_data_hash(db)

        #create the graph
        graph = cls.__initiate_graph(people_and_sector_list)
        graph.set_name_map()

        #work on graph
        cls.__set_all_affinities_to_zero()
        cls.__insert_data(graph, data_hash_of_hash)

        return graph

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
    def __set_all_affinities_to_zero(cls, graph: Graph) -> None:
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
        """
        Set the affinity to all nodes -> n^2
        """
        for origin, message_list in data_hash_of_hash:
            for message in message_list:
                text = message["text"]
                destiny_node = graph.adjacency_list[graph.name_map[message["destiny"]]]
                actual_graph_node = graph.adjacency_list[graph.name_map[origin]]
                affinity = cls.calculate_affinity_based_on_text_size(text)
                new_tup = (destiny_node, actual_graph_node.adjacency_list[1] + affinity)
                actual_graph_node.adjacency_list = new_tup

    @classmethod
    def calculate_affinity_based_on_text_size(cls, text):
        return len(text)**(2/3)
