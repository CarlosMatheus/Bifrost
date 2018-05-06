
class Handler:
    slack_client = None

    @classmethod
    def set_client(cls, slack_client):
        cls.slack_client = slack_client

    @classmethod
    def run_user_queue(cls):
        pass

    @classmethod
    def handle_event(cls, message, event):
        pass