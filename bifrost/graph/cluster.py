from typing import List, Tuple


class Element:
    '''
        Class representation of an element of the clutering space
    '''

    def __init__(self, node: Node, thrs: float) -> None:
        self.thrs = thrs
        self.node = node

    def dist(self, other: 'Element') -> float:
        # dist = thrs - affinity
        return self.thrs - self.node.affinity_hash[other.node]


class Cluster:
    '''
        Set of close elements that are grouped as a single entity.
        Represent a set of users with relevant social interaction
    '''

    def __init__(self, elems: List[Element]) -> None:
        self.elements = elems

    @property
    def size(self) -> int:
        return len(self.elements)

    @property
    def dispersion(self) -> float:
        '''
            The dispersion of a cluster is a measure of the clustering error
        :return: The cluster dispersion
        '''
        disp = 0.0
        for elem in self.elements:
            for elem2 in self.elements:
                if elem is not elem2:
                    disp += elem.dist(elem2)
        disp /= 2  # distances were counted twice
        return disp


class ClusterGroup:
    '''
        Clustering space
    '''

    STOP_THRS = 10  # Minimal dispersion error needed to avoid 2 clusters' merge

    def __init__(self, graph: Graph) -> None:
        self.graph = graph  # Reference to graph bijection
        self.thrs = graph.greatest_edge() # Maximum distance between any two elements of the space

        self.all_elements = self.__create_elements(graph)
        self.elem_dist_matrix = {}
        self.__calc_elem_dists()

        self.clusters = []
        self.cluster_dist_matrix = {}

        # self.tf_elements = tf.constant(self.elements)
        #self.tf_clusters = []

    def __create_elements(self, graph: Graph) -> List[Element]:
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
        for elem in self.all_elements:
            self.elem_dist_matrix[elem] = {}
            for other_elem in self.all_elements:
                if other_elem is not elem:
                    self.elem_dist_matrix[elem][other_elem] = self.dist_fn(elem, other_elem)

    def dist_fn(self, elem_a: Element, elem_b: Element) -> float:
        '''
            Implementation of distance metric in the space of elements
        :param elem_a: some element
        :param elem_b: some other nice element
        :return: the distance metric between elem_a and elem_b
        '''
        if elem_a is None or elem_b is None:
            raise ValueError
        # TODO: Consider other parameters than direct edge distance???
        return elem_a.dist(elem_b)

    def cluster_dist(self, cluster_a: Cluster, cluster_b: Cluster) -> float:
        '''
            Compute cluster interdistance without any centroid information.
            O(cluster_a.size * cluster_b.size)
        :param cluster_a: some cluster
        :param cluster_b: some other cluster
        :return: the distance between clusters a and b(mean distance between elems)
        '''
        if cluster_a is None or cluster_b is None:
            raise ValueError

        if self.cluster_dist_matrix.get(cluster_a) is not None and self.cluster_dist_matrix[cluster_a].get(cluster_b) is not None:
            return self.cluster_dist_matrix[cluster_a][cluster_b]

        total_dist = 0.0
        for elem_a in cluster_a.elements:
            for elem_b in cluster_b.elements:
                total_dist += self.elem_dist_matrix[elem_a][elem_b]
        total_dist /= 2  # edges were counted twice
        total_dist /= (cluster_a.size + cluster_b.size)

        if self.cluster_dist_matrix.get(cluster_a) is None:
            self.cluster_dist_matrix[cluster_a] = {}
        if self.cluster_dist_matrix.get(cluster_b) is None:
            self.cluster_dist_matrix[cluster_b] = {}
        self.cluster_dist_matrix[cluster_a][cluster_b] = total_dist
        self.cluster_dist_matrix[cluster_b][cluster_a] = total_dist

        return total_dist

    def merge_clusters(self, cluster_a: Cluster, cluster_b: Cluster) -> None:
        '''
            Combine elements of two distinct clusters into one single bigger cluster
        :param cluster_a: a cluster
        :param cluster_b: some other cluster
        :return: merged cluster from cluster_a and cluster_b
        '''

        if cluster_a is None or cluster_b is None:
            raise ValueError
        if cluster_a is cluster_b:
            raise ValueError

        self.clusters.remove(cluster_a)
        self.clusters.remove(cluster_b)
        if self.cluster_dist_matrix.get(cluster_a):
            del self.cluster_dist_matrix[cluster_a]
        if self.cluster_dist_matrix.get(cluster_b):
            del self.cluster_dist_matrix[cluster_b]
        self.clusters.append(Cluster(cluster_a.elements + cluster_b.elements))

    def nearest_clusters(self) -> Tuple[Cluster, Cluster]:
        '''
            Finds pair of clusters with minimal distance between each other
        :return: Tuple with the two nearest clusters
        '''
        if len(self.clusters) < 2:
            raise RuntimeError('Clustering space has less 2 clusters')
        cluster_a = None
        cluster_b = None
        min_dist = None
        for ca in self.clusters:
            for cb in self.clusters:
                if ca is not cb:
                    dist = self.cluster_dist(ca, cb)
                    if min_dist is None or dist < min_dist:
                        cluster_a = ca
                        cluster_b = cb
                        min_dist = dist
        return cluster_a, cluster_b

####################################################################
####################################################################

    def cluster(self) -> List[Cluster]:
        '''
            Do clustering algorithm (Hierarchical Clustering)
        :return: List of clusters of optimized elements' correlation
        '''
        if self.graph.size < 1:
            return []
        self.__init_clusters()

        for i in range(0, self.graph.size-1):
            cluster_a, cluster_b = self.nearest_clusters()
            new_cluster = Cluster(cluster_a.elements + cluster_b.elements)
            if new_cluster.dispersion > ClusterGroup.STOP_THRS:
                break
            self.merge_clusters(cluster_a, cluster_b)
        return self.clusters

    def __init_clusters(self) -> None:
        '''
            Inits primitive one-element clusters
        :return:
        '''
        for elem in self.all_elements:
            self.clusters.append(Cluster([elem]))
        # self.tf_clusters = tf.Variable(self.clusters)




