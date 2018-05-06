from .event_handler import Handler
from db_manager import DbManager
from .parser import Parser
from .default_messages import DefaultMessages


class User:
    user_dict = {}

    def __init__(self, data, team):
        self.id = data["id"]
        self.real_name = data["real_name"]
        self.name = data["name"]
        self.profile_name = data["profile"]["display_name"]
        self.team = team

        # Flow control variables
        self.ready_to_send = False
        self.stored_message = ""

    def __str__(self):
        return self.name

    def answer(self, text):
        Handler.post(text, self.id)

    def add_message(self, message_original):
        if not (self.ready_to_send):
            user_id, message = Parser.parse_direct_mention(message_original)

            if user_id is None:
                response = "-1"
                message = message_original
            else:
                response = user_id

            self.answer("Tem certeza que quer mandar?\n " + message + "\n Se sim digite sim")

            self.stored_message = message_original
            self.ready_to_send = True

        else:
            if message_original == "sim":
                self.add_message_to_database(self.stored_message)
            else:
                self.answer("A mensagem não será enviada")
            self.ready_to_send = False

    def add_message_to_database(self, message_original):

        user_id, message = Parser.parse_direct_mention(message_original)

        if user_id is None:
            response = "-1"
            message = message_original
        else:
            response = user_id

        DbManager.add_to_today(self.id, response, message)

        if user_id is None:
            self.answer(DefaultMessages.default_thanks())
        else:
            self.answer(DefaultMessages.custom_thanks(User.user_dict[user_id].real_name))




