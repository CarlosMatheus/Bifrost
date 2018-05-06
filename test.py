from db_manager import DbManager
from graph.graph_maker import GraphMaker

if __name__ == "__main__":
    DbManager.init_db()
    DbManager.add_to_today("batata1", "teste1", "oieeee")
    DbManager.add_to_today("batata2", "teste2", "xaau")
    DbManager.add_to_today("batata2", "teste1", "xaau")
    DbManager.add_to_user_list("oi", "xau")
    DbManager.add_to_user_list("oi2", "xau2")
    print(DbManager.read_from_ul())
    #a = GraphMaker.create_graph([{"name":"batata1", "sector":"oi"}, {"name":"batata2", "sector": "xau"}, {"name":"teste1", "sector":"oi"}, {"name":"teste2", "sector":"oi"}], DbManager.read_from_db())
    #print(a)
