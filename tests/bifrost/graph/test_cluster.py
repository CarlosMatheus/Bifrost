from bifrost.graph.graph_maker import *
from bifrost.graph.cluster import *
from bifrost.data_managers.db_manager import *

if __name__ == '__main__':
    DbManager.init_db()

    people = [ 'felipe', 'shark', 'coe', 'aloysio']

    for name in people:
        DbManager.add_to_user_list(name, 'marketing')

    DbManager.add_to_today('felipe', 'shark', 'oi shark')
    DbManager.add_to_today('felipe', 'coe', 'quie')
    DbManager.add_to_today('felipe', 'aloysio', 'porra aloysio')
    DbManager.add_to_today('coe', 'aloysio', 'olha so o pirata haha')

    g = GraphMaker.create_graph(DbManager.read_from_ul(), DbManager.read_from_db())
    for node in g.adjacency_list:
        pass

    cg = ClusterGroup(g)
    clusters = cg.cluster()
    for c in clusters:
        pass
