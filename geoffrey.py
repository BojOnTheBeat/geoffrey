import os
import time
from slackclient import SlackClient 

BOT_ID = os.environ.get("GEOFFREY_ID")

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"


#instantiate Slack client
slack_client = SlackClient(os.environ.get('GEOFFREY_BOT_TOKEN'))

def handle_command(command, channel):
	"""
		Receives commands directed at the bot and deterimines if they
		are valid commands. If so, then acts on the commands. If not,
		returns back what it needs for clarification
	"""
	response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
			   "* command with numbers, separated by spaces."

	if command.startswith(EXAMPLE_COMMAND):
		response = "I don't know how to do that yet, I'm still learning"
	slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
	"""
		The Slack Real Time Messaging API is an events firehose.
		This parsing function returns None unless a message is 
		directed at the Bot, based on its ID
	"""
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				# return text after the @ mention, remove the whitespace
				return output['text'].split(AT_BOT)[1].strip().lower(), \
					   output['channel']
	return None, None


if __name__ == '__main__':
	READ_WEBSOCKET_DELAY = 1 #1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("Geoffrey connected and running!")
		while True:
			command, channel = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				handle_command(command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")

