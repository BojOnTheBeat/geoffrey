import os
from slackclient import SlackClient


BOT_NAME = 'geoffrey'


slack_client = SlackClient(os.environ.get('GEOFFREY_BOT_TOKEN')) #token is an environment variable


if __name__ == '__main__':
	api_call = slack_client.api_call("users.list")

	if api_call.get('ok'):
		# retrieve all users so we can find our bot

		users = api_call.get('members')
		for user in users:
			if 'name' in user and user.get('name') == BOT_NAME:
				print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
	else:
		print("Cannot find a bot with name: '" + BOT_NAME + "'")
