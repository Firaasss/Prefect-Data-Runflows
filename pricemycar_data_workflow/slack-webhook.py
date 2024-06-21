from prefect import flow
from prefect_slack import SlackWebhook
from prefect_slack.messages import send_incoming_webhook_message
from prefect.blocks.notifications import SlackWebhook

@flow
def example_slack_send_message_flow():
    slack_webhook = SlackWebhook.load("slack-webby")
    result = send_incoming_webhook_message(
        slack_webhook=slack_webhook,
        text="This proves send_incoming_webhook_message works!",
    )
    return result

example_slack_send_message_flow()