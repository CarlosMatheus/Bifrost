from .parser import Parser
from .default_messages import DefaultMessages
from db_manager import DbManager
from graph.graph_maker import GraphMaker
from graph.cluster import *
from graph.cluster_suggester import ClusterSuggester
from typing import List
import networkx as nx
import matplotlib.pyplot as plt
import threading

class Handler:
    slack_client = None
    bot_id = None
    users = None
    response_list = []
    now =  False

    @classmethod
    def set_client(cls, slack_client):
        cls.slack_client = slack_client

    @classmethod
    def send_suggested(cls, to_user, from_user):
        print(cls.users[to_user], " ", cls.users[from_user])
        cls.users[to_user].answer("Você conhece o " + cls.users[from_user].real_name+"? Porque não enviar uma mensagem para ele?")

    @classmethod
    def set_bot(cls, bot_id):
        cls.bot_id =bot_id

    @classmethod
    def set_users(cls, users):
        cls.users = users

    @classmethod
    def run_user_queue(cls):
        while len(cls.response_list) > 0:
            element = cls.response_list.pop(0)
            channel = cls.slack_client.api_call('im.open', user=element[1])
            if channel is not None:
                channel = channel["channel"]["id"]
                cls.slack_client.api_call('chat.postMessage', channel=channel,
                                      text=element[0])

    @classmethod
    def send_daily_messages(cls):
        for user in cls.users:
            person = cls.users[user]
            while len(DbManager.check_for_msg(person.id)) > 0:
                text = DbManager.send_msg(person.id)
                person.answer('Você recebeu uma mensagem:\n'+text)

    @classmethod
    def handle_event(cls, message, event):

        if event["channel"].startswith("D"):
            if message.startswith("\\"):
                cls.handle_command(message, event)

            else:
                cls.users[event["user"]].add_message(message)

        user_id, message = Parser.parse_direct_mention(message)

        if user_id == cls.bot_id:
            cls.slack_client.api_call('chat.postMessage', channel=event["channel"],
                                      text=DefaultMessages.contact_on_direct())

    @classmethod
    def post(cls, message, channel):
        cls.response_list += [(message, channel)]

    @classmethod
    def handle_command(cls, command, event):

        user = cls.users[event["user"]]

        words = command.split(" ")

        if len(words) > 1:
            user.answer("Invalid command")

        elif words[0] == "\\ajuda":
            user.answer(DefaultMessages.mensagem_ajuda())
        elif words[0] == "\\comandos":
            user.answer(DefaultMessages.mensagem_comandos())
        elif words[0] == "\\now":
            cls.now = True
        elif words[0] == "\\alg":
            cls.run_algorithm()

    @classmethod
    def run_algorithm(cls):
        g = GraphMaker.create_graph(DbManager.read_from_ul(), DbManager.read_from_db())
        cg = ClusterGroup(g)
        clusters = cg.cluster()
        cls.debug_clusters(clusters)
        cls.visual_debug(cg)
        ClusterSuggester.make_suggestion(cg)

    @classmethod
    def visual_debug(cls, cg: ClusterGroup):
        graph = nx.Graph()
        for elem1,elems in cg.elem_dist_matrix.items():
            for elem2, value in elems.items():
                graph.add_edge(cls.users[elem1.node.name].name, cls.users[elem2.node.name].name, weight=value)

        #t = threading.Thread(target=cls.plot, args=(graph,))
        #t.start()
        plt.subplot(111)
        nx.draw(g, with_labels=True)
        plt.show()


    @classmethod
    def plot(cls, g):
        plt.subplot(111)
        nx.draw(g, with_labels=True)
        plt.show()

    @classmethod
    def debug_clusters(cls, clusters: List[Cluster]):
        print("Found", len(clusters), "clusters")
        for i in range(0,len(clusters)):
            names = []
            for elem in clusters[i].elements:
                names += [elem.node.name]
            print("Cluster", i, "(disp=",clusters[i].dispersion(),":", ' '.join([cls.users[x].name for x in names]))
