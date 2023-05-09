import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

log = logging.getLogger(__name__)

# SLACK SETTINGS
root_dir = os.path.dirname(__file__)
SLACK_TMP_FILE = os.path.join(root_dir, "TMP.txt")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

class SlackApi(object):
    def __init__(self, token=SLACK_BOT_TOKEN):
        self.client = WebClient(token)

    def send_txt(self, text, attachments, channel_id=SLACK_CHANNEL_ID):
        try:
            result = self.client.chat_postMessage(
                channel=channel_id,
                text=text,
                attachments=attachments if attachments else [],
            )
            log.debug(result)
        except SlackApiError as error:
            log.exception(f"{error = }")
            exit(1)

    def upload_file(
        self, file_name, text="Attached file :smile:", channel_id=SLACK_CHANNEL_ID
    ):
        try:
            result = self.client.files_upload(
                channels=channel_id,
                initial_comment=text,
                file=file_name,
            )
            log.debug(result)
        except SlackApiError as error:
            log.exception(f"{error = }")
            exit(1)

    @staticmethod
    def get_markdown_attachment_template(
        text: str = "No Data", message_type: str = "plain_text"
    ):
        """
        message_type = ['mrkdwn', 'plain_text']
        """
        return [
            {
                "blocks": [
                    {"type": "section", "text": {"type": message_type, "text": text}}
                ]
            }
        ]
