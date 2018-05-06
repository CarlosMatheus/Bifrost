from typing import List
from graph.graph import *
from graph.node import *
import tensorflow as tf


class Element:

    def __init__(self, node: Node=None, thrs: float=0.0) -> None:
        self.thrs = thrs
        self.node = node

    def dist(self, other: 'Element') -> float:
        # dist = thrs - affinity
        return self.thrs - self.node.affinity_hash[other.node]


class Cluster:

    def __init__(self, elems: List[Element]) -> None:
        self.elements = elems
        self.centroid = None

    @property
    def size(self) -> int:
        return len(self.elements)

    def dispersion(self):
        disp = 0.0
        for elem in self.elements:
            for elem2 in self.elements:
            if elem is not elem2:
                disp += elem.dist(elem2)
        disp /= 2 # distances are counted twice
        return disp

    def update_centroid(self):
        pass


class ClusterGroup:

    STOP_THRS = 10 ## Cards
    MAX_ITER = 1000 ## Cards

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.thrs = graph.greatest_edge()

        self.elements = ClusterGroup.create_elements(graph)
        #self.tf_elements = tf.constant(self.elements)

        self.clusters = []
        #self.tf_clusters = []

        self.elem_dist_matrix = {}
        self.__calc_elem_dists()
        self.cluster_dist_matrix = {}

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

    def __calc_elem_dists(self) -> None:
        '''
            Fills matrix of distances between elements
        :return:
        '''
        for elem in self.elements:
            self.elem_dist_matrix[elem.node.name] = {}
            for other_elem in self.elements:
                if other_elem is not elem:
                    self.elem_dist_matrix[elem.node][other_elem.node] = self.dist_fn(elem, other_elem)

    def dist_fn(self, elem_a: Element, elem_b: Element) -> float:
        '''
            Implementation of distance metric in the space of elements
        :param elem_a: some element
        :param elem_b: some other nice element
        :return: the distance metric between elem_a and elem_b
        '''
        # TODO: Consider other parameters than direct edge distance???
        return elem_a.dist(elem_b)

    def cluster_dist(self, cluster_a: Cluster, cluster_b: Cluster) -> float:
        '''
            O(cluster_a.size * cluster_b.size)
        :param cluster_a: some pretty cluster
        :param cluster_b: some other pretty cluster
        :return: the distance between clusters a and b(mean distance between elems)
        '''
        ## TODO: HOW THE HELL TO COMPUTE CLUSTER DISTANCE WITHOUT 2 FUCKING LOOPS
        if self.cluster_dist_matrix.get(cluster_a) is not None and self.cluster_dist_matrix[cluster_a].get(cluster_b) is not None:
            return self.cluster_dist_matrix[cluster_a][cluster_b]

        total_dist = 0.0
        for elem_a in cluster_a.elements:
            for elem_b in cluster_b.elements:
                total_dist += self.elem_dist_matrix[elem_a][elem_b]
        total_dist /= 2 # edges are counted twice
        total_dist /= (cluster_a.size + cluster_b.size)

        if self.cluster_dist_matrix.get(cluster_a) is None:
            self.cluster_dist_matrix[cluster_a] = {}
        if self.cluster_dist_matrix.get(cluster_b) is None:
            self.cluster_dist_matrix[cluster_b] = {}
        self.cluster_dist_matrix[cluster_a][cluster_b] = total_dist
        self.cluster_dist_matrix[cluster_b][cluster_a] = total_dist

        return total_dist

    def merge_clusters(self, cluster_a: Cluster, cluster_b: Cluster) -> None:
        self.clusters.remove(cluster_a)
        self.clusters.remove(cluster_b)
        if self.cluster_dist_matrix.get(cluster_a):
            del self.cluster_dist_matrix[cluster_a]
        if self.cluster_dist_matrix.get(cluster_b):
            del self.cluster_dist_matrix[cluster_b]
        self.clusters.append(Cluster(cluster_a.elements + cluster_b.elements))

####################################################################
####################### Hierarchical Clustering ####################
####################################################################
    def cluster(self) -> List[Cluster]:
        '''
            Do clustering algorithm(Hierarchical Clustering)
        :return: List of clusters of optimized elements' correlation
        '''
        self.__init_clusters()

        for i in range(self.graph.size)

        return self.clusters

    def __init_clusters(self) -> None:
        '''
            Inits primitive one-element clusters
        :return:
        '''
        for elem in self.elements:
            self.clusters.append(Cluster([elem]))
        #self.tf_clusters = tf.Variable(self.clusters)



