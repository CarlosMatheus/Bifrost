import os
import time
from slackclient import SlackClient
from bot.parser import Parser


def get_id_from_name(name):
    for user in users_list:
        if user["id"] == name:
            return user["real_name"]


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


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

        # Bot main loop

        while True:
            message, event = Parser.parse_bot_commands(slack_client.rtm_read())

            if event:
                handle_command(None, None)
            time.sleep(RTM_READ_DELAY)

    else:
        print("Connection failed. Exception traceback printed above.")