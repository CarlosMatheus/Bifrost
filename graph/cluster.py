from typing import List
from graph.graph import *
from graph.node import *
import tensorflow as tf


class Element:

    def __init__(self, node: Node, thrs: float) -> None:
        self.thrs = thrs
        self.node = node

    def dist(self, other: 'Element') -> float:
        # dist = thrs - affinity
        pass


class Cluster:

    def __init__(self, elems: List[Element]) -> None:
        self.elements = elems
        self.centroid = None

    @property
    def size(self) -> int:
        return len(self.elements)

    def dist(self, other: 'Cluster') -> float:
        pass


class ClusterGroup:

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.thrs = graph.greatest_edge()

        self.elements = ClusterGroup.create_elements(graph)
        self.tf_elements = tf.constant(self.elements)

        self.clusters = []
        self.tf_cluster = []
        self.elem_dist_matrix = {}
        self.cluster_dist_matrix = {}

    @classmethod
    def create_elements(self, graph: Graph) -> List[Element]:
        '''
        :param graph:
        :return: list of elements
        '''
        if graph is not None:
            elem_list = []
            for node in graph.adjacency_list:
                elem_list.append(Element(node, self.thrs))
            return elem_list

    def calc_elem_dists(self) -> None:
        '''
            Fills matrix of distances between elements
        :return:
        '''
        for elem in self.elements:
            self.elem_dist_matrix[elem.node.name] = {}
            for other_elem in self.elements:
                if other_elem is not elem:
                    self.elem_dist_matrix[elem.node.name][other_elem.node.name] = self.dist_fn(elem, other_elem)

    def dist_fn(self, elem_a: Element, elem_b: Element) -> float:
        '''
            Implementation of distance metric in the space of elements
        :param elem_a: some element
        :param elem_b: some other nice element
        :return: the distance metric between elem_a and elem_b
        '''
        # Consider other parameters than direct edge distance???
        return elem_a.dist(elem_b)

    def cluster(self) -> None:
        '''
        Does clustering algorithm(Hierarchical Clustering)
        :return:
        '''
        self.__start_clusters()
        self.__update_cluster_dists()
        self.__do_cluster()

    def __start_clusters(self) -> None:
        for elem in self.elements:
            self.clusters.append(Cluster([elem]))

    def __update_cluster_dists(self):
        pass

    def __do_cluster(self):
        pass

