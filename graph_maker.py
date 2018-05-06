from graph import Graph


class GraphMaker:

    @classmethod
    def create_graph(cls, pyrebase, people_list):
        db = pyrebase.database()
        data_hash = cls.__get_data_hash(db)
        graph = cls.__initiate_graph(people_list)

    @classmethod
    def __initiate_graph(cls, people_list):
        g = Graph()
        for person in people_list:
            g.adjacency_list.append(person)
        return g

    @classmethod
    def __get_data_hash(cls, db):
        #todo
        # Return the hash with the data
        return 0

    @classmethod
    def __insert_data(cls, graph, data_hash):



