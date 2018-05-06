import os
import time
from slackclient import SlackClient
from bot.parser import Parser
from bot.event_handler import Handler


if __name__ == "__main__":

    # Instantiating the client
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    # Bot id
    bot_id = None

    # Users names

    users_names = None

    # Constants
    RTM_READ_DELAY = 1

    EXAMPLE_COMMAND = 'do'

    if slack_client.rtm_connect(with_team_state=False):
        print("Thor connected and running!")

        # Read bot's user ID by calling Web API method `auth.test`
        bot_id = slack_client.api_call("auth.test")["user_id"]

        # Getting users names
        users_list = slack_client.api_call('users.list')['members']
        users_names = [x["name"] for x in users_list]

        # Initializing parser

        Parser.set_client(slack_client)

        # Initializing handler

        Handler.set_client(slack_client)

        # Bot main loop

        while True:
            message, event = Parser.parse_bot_commands(slack_client.rtm_read())

            if event:
                Handler.handle_event(message, event)

            Handler.run_user_queue()

            time.sleep(RTM_READ_DELAY)

    else:
        print("Connection failed. Exception traceback printed above.")