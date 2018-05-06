from .parser import Parser
from .default_messages import DefaultMessages
class Handler:
    slack_client = None
    bot_id = None
    response_list = []

    @classmethod
    def set_client(cls, slack_client):
        cls.slack_client = slack_client

    @classmethod
    def set_bot(cls, bot_id):
        cls.bot_id =bot_id

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
    def handle_event(cls, message, event):

        if event["channel"].startswith("D"):
            print("aqui")

        user_id, message = Parser.parse_direct_mention(message)

        if user_id == cls.bot_id:
            cls.slack_client.api_call('chat.postMessage', channel=event["channel"],
                                      text=DefaultMessages.contact_on_direct())

    @classmethod
    def post(cls, message, channel):
        cls.response_list += [(message, channel)]