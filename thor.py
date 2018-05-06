import os
import time
import datetime
from db_manager import DbManager
from slackclient import SlackClient
from bot.parser import Parser
from bot.user import User
from bot.event_handler import Handler
from bot.default_messages import DefaultMessages


def handler(message):
    if message["event"] == "put":
        data = message["data"]
        Handler.send_suggested(data["sender"], data["receiver"])


if __name__ == "__main__":

    # Initializing database

    DbManager.init_db()
    DbManager.listen_to_suggested(handler)
    DbManager.add_to_suggested("UAK11AA4S", "UAL39CRNK")

    # Instantiating the client

    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    # Bot id
    bot_id = None

    # Users names

    users_names = None

    # Constants
    RTM_READ_DELAY = 0.02

    delay = datetime.timedelta(minutes=30)

    # Current data

    today = datetime.datetime.today()

    if slack_client.rtm_connect(with_team_state=False):
        print("Thor connected and running!")

        # Read bot's user ID by calling Web API method `auth.test`
        bot_id = slack_client.api_call("auth.test")["user_id"]

        # Getting users names
        users_list = slack_client.api_call('users.list')['members']

        User.user_dict = {}

        for user in users_list:
            if user["id"] != bot_id:
                User.user_dict[user["id"]] = User(user, slack_client.api_call('team.info', id=user["team_id"])["team"]["name"])
                DbManager.add_to_user_list(user["id"], slack_client.api_call('team.info', id=user["team_id"])["team"]["name"])

        # Initializing parser

        Parser.set_client(slack_client)

        # Initializing handler

        Handler.set_client(slack_client)
        Handler.set_bot(bot_id)
        Handler.set_users(User.user_dict)

        # Bot main loop

        while True:
            message, event = Parser.parse_bot_commands(slack_client.rtm_read())

            if event:
                Handler.handle_event(message, event)

            if today + delay < datetime.datetime.today():
                for key in User.user_dict:
                    User.user_dict[key].answer(DefaultMessages.send_daily())
                Handler.send_daily_messages()
                today = datetime.datetime.today()

            Handler.run_user_queue()

            time.sleep(RTM_READ_DELAY)

    else:
        print("Connection failed. Exception traceback printed above.")