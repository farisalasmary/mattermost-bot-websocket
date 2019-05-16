"""
    @author
          ______         _                  _
         |  ____|       (_)           /\   | |
         | |__ __ _ _ __ _ ___       /  \  | | __ _ ___ _ __ ___   __ _ _ __ _   _
         |  __/ _` | '__| / __|     / /\ \ | |/ _` / __| '_ ` _ \ / _` | '__| | | |
         | | | (_| | |  | \__ \    / ____ \| | (_| \__ \ | | | | | (_| | |  | |_| |
         |_|  \__,_|_|  |_|___/   /_/    \_\_|\__,_|___/_| |_| |_|\__,_|_|   \__, |
                                                                              __/ |
                                                                             |___/
            Email: farisalasmary@gmail.com
            Date:  May 15, 2019
"""

from mattermostdriver import Driver
import requests
import asyncio
import json
import config

####################################################################################################################################################################################
def send_message(text, sender_name):
    data = {
      'payload': '{"channel": "@' + sender_name + '", "text": "' + text + '", "icon_url": "' + config.AVATAR_URL + '"}'
    }

    response = requests.post(config.MATTERMOST_INCOMING_WEBHOOK, data=data)
####################################################################################################################################################################################
@asyncio.coroutine
def event_handler(message):
    message_obj = json.loads(message)
    if 'event' in message_obj.keys():
        if message_obj['event'] == 'posted':
            if 'channel_display_name' in message_obj['data'].keys():
                public_channels = []
                for team in config.TEAMS:
                    team_id = driver.teams.get_team_by_name(team)['id']
                    user_id = driver.users.get_user_by_username(config.MY_NAME)['id']
                    public_channels += [i['display_name'] for i in driver.channels.get_channels_for_user(user_id, team_id) if i['display_name'] != '']
                
                if message_obj['data']['channel_display_name'] not in public_channels:
                    if 'post' in message_obj['data'].keys() and 'sender_name' in message_obj['data'].keys():
                        sender_name = message_obj['data']['sender_name']
                        message = 'UNKOWN'
                        post_obj = json.loads(message_obj['data']['post'])
                        if 'message' in post_obj.keys():
                            message = post_obj['message']        # sender's message
                            if sender_name != config.MY_NAME:    # VERY IMPORTANT TO ADD THIS LINE TO PREVENT INFINITE LOOP
                                # NOTE: all lines of code above are to extract the message that was sent to the bot and its sender name
                                get_bot_response(message, sender_name)
####################################################################################################################################################################################
def get_bot_response(message, sender_name):
    my_message = 'welcome!!!!!!!!!'
    send_message(my_message, sender_name)

####################################################################################################################################################################################
if __name__ == '__main__':
    driver = Driver(
                    {
                        
                        'url': config.MATTERMOST_SERVER_URL,
                        'login_id': config.USERNAME,
                        'password': config.PASSWORD,
                        'scheme': 'http',
                        'port': config.MATTERMOST_SERVER_PORT,
                        'basepath': '/api/v4',
                        'verify': False,
                        'timeout': 30,
                        'debug': False
                    }
                )

    # login into the Mattermost server
    driver.login()
    
    # establish a websocket connection and keep listining to ALL events
    driver.init_websocket(event_handler)



