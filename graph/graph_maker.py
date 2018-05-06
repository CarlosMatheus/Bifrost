from graph.graph import Graph
from graph.node import Node


class GraphMaker:

    @classmethod
    def create_graph(cls, people_and_sector_list: list, data_hash_of_hash: dict) -> Graph:
        # Create the graph
        graph = cls.__initiate_graph(people_and_sector_list)
        graph.set_name_map()

        # Work on graph
        cls.__set_all_affinities_to_zero(graph)
        cls.__insert_data(graph, data_hash_of_hash)
        cls.__match_data(graph)

        return graph

    @classmethod
    def __initiate_graph(cls, people_and_sector_list: list) -> Graph:
        g = Graph()
        for elem in people_and_sector_list:
            name = elem["name"]
            sector = elem["sector"]
            g.adjacency_list.append(Node(name, sector))
        return g

    @classmethod
    def __set_all_affinities_to_zero(cls, graph: Graph):
        """
        n^2 alg -> set all node adjacent list to all other nodes having affinity zero
        """
        for node in graph.adjacency_list:
            for node_to_add in graph.adjacency_list:
                if node_to_add != node:
                    node.affinity_hash[node_to_add] = 0
                    node.adj_vertices.append(node_to_add)

    @classmethod
    def __insert_data(cls, graph: Graph, data_hash_of_hash: dict) -> None:
        """
        Set the affinity to all nodes -> n^2
        """
        for origin, message_list in data_hash_of_hash:
            actual_graph_node = graph.adjacency_list[graph.name_map[origin]]
            for message in message_list:
                text_str = message["text"]
                destiny_str = message["receiver"]
                destiny_idx = graph.name_map[destiny_str]
                destiny_node = graph.adjacency_list[destiny_idx]
                affinity = cls.__calculate_affinity_based_on_text_size(text_str)
                actual_graph_node.affinity_hash[destiny_node] += affinity

    @classmethod
    def __calculate_affinity_based_on_text_size(cls, text: str) -> float:
        return (len(text)**(2/3))

    @classmethod
    def __match_data(cls, graph: Graph):
        """
        make the both directions of the graph have the same value
        """
        for actual_node in graph.adjacency_list:
            for node in actual_node.adj_vertices:
                affinity = (node.affinity_hash[actual_node] + actual_node.affinity_hash[node])/2
                node.affinity_hash[actual_node] = affinity
                actual_node.affinity_hash[node] = affinity
