from .event_handler import Handler

class User:
    def __init__(self, data, team):
        self.id = data["id"]
        self.real_name = data["real_name"]
        self.name = data["name"]
        self.team = team

    def __str__(self):
        return "Name: " + self.name + ", Team: " + self.team

    def answer(self, text):
        Handler.post(text, self.id)


