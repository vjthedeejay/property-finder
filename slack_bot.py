from slackclient import SlackClient

class SlackBot:
    """
    Class that creates a slack bot that posts messages to a channel
    """
    def __init__(self, config):
        """
        Set instance attributes and create slack client
        """
        self.config = config

        self.slack_client = SlackClient(self.config.SLACK_TOKEN)

    def post_to_channel(self, text):
        """
        Post to Slack channel defined in configuration
        """
        self.slack_client.api_call(
            "chat.postMessage",
            channel=self.config.SLACK_CHANNEL,
            text=text,
            username='pybot',
            icon_emoji=':robot_face:'
        )