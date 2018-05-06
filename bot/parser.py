import re


class Parser:
    slack_client = None
    MENTION_REGEX = '^<@(|[WU].+?)>(.*)'

    @classmethod
    def set_client(cls, slack_client):
        cls.slack_client = slack_client

    @classmethod
    def parse_direct_mention(cls, message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(cls.MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    @classmethod
    def parse_bot_commands(cls, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                # user_id, message = cls.parse_direct_mention(event["text"])
                # print(event["channel"], " ", event["user"])

                #t = cls.slack_client.api_call('im.open', user=event["user"])

                #t = t["channel"]["id"]

                message = event['text']

                if event['channel'].startswith("D"):
                    return message, event

        return None, None
