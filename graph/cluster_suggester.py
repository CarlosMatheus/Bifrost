from db_manager import DbManager


class ClusterSuggester:

    suggestions = dict()

    @classmethod
    def make_suggestion(cls, cg):
        cluster_arr = cg.clusters
        cls.suggestions = dict()
        for cluster in cluster_arr:
            min_dist_cluster = cls.__get_closest_cluster(cluster, cluster_arr, cg)
            if min_dist_cluster is not None:
                cls.__make_recommendations(cluster, min_dist_cluster)
        cls.__pass_suggestions()

    @classmethod
    def __get_closest_cluster(cls, cluster, cluster_list, cg):
        min = 1000000
        min_dist_cluster = None
        for other_cluster in cluster_list:
            if other_cluster != cluster:
                dist = cg.cluster_dist(cluster, other_cluster)
                if dist < min:
                    min = dist
                    min_dist_cluster = other_cluster
        return min_dist_cluster

    @classmethod
    def __make_recommendations(cls, cluster1, cluster2):
        max_dist = 0
        max_dist_elements = None
        for elem1 in cluster1.elements:
            for elem2 in cluster2.elements:
                dist = elem1.dist(elem2)
                if dist > max_dist:
                    max_dist = dist
                    max_dist_elements = (elem1, elem2)
        if max_dist_elements is not None:
            if cls.__has_not_suggested(max_dist_elements, cls.suggestions):
                cls.suggestions[max_dist_elements[0]] = max_dist_elements[1]
                cls.suggestions[max_dist_elements[1]] = max_dist_elements[0]

    @classmethod
    def __has_not_suggested(cls, tup_ele, suggestions):
        if suggestions.get(tup_ele[0]) is not None:
            if suggestions[tup_ele[0]] == tup_ele[1]:
                return False
        if suggestions.get(tup_ele[1]) is not None:
            if suggestions[tup_ele[1]] == tup_ele[0]:
                return False
        return True

    @classmethod
    def __pass_suggestions(cls):
        alredy_added = dict()
        for node1, node2 in cls.suggestions.items():
            tup = (node1, node2)
            if cls.__has_not_suggested(tup, alredy_added):
                DbManager.add_to_suggested(node1.node.name, node2.node.name)
            alredy_added[node1] = node2
            alredy_added[node2] = node1
