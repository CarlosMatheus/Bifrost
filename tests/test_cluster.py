from graph.graph import *
from graph.graph_maker import *
from graph.cluster import *
from db_manager import *

if __name__ == '__main__':
    DbManager.init_db()

    people = [ 'felipe', 'shark', 'coe', 'aloysio']

    for name in people:
        DbManager.add_to_user_list(name, 'marketing')

    DbManager.add_to_today('felipe', 'shark', 'f - s')
    DbManager.add_to_today('felipe', 'coe', 'f - c')
    DbManager.add_to_today('felipe', 'aloysio', 'f - a')
    DbManager.add_to_today('coe', 'aloysio', 'c - a')

    g = GraphMaker.create_graph(DbManager.read_from_ul(), DbManager.read_from_db())
    print(g)