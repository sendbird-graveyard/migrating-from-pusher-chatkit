from dateutil.parser import parse
from pathlib import Path
import json
import os

import ijson


INPUT_PUSHER_PATH = '_input'
OUTPUT_SENDBIRD_PATH = '_output'
if not Path(INPUT_PUSHER_PATH).is_dir():
    os.mkdir(INPUT_PUSHER_PATH)

if not Path(OUTPUT_SENDBIRD_PATH).is_dir():
    os.mkdir(OUTPUT_SENDBIRD_PATH)

################################################
# USER
################################################
PUSHER_USER_FILENAME = 'users.json'
USERS_PER_FILE = 10000
SENDBIRD_USER_FILENAME = 'exported_sendbird_users'


def init_user():
    user = {
        'user_id': '',
        'nickname': '',
        'profile_url': '',
        'profile_file': '',
        'metadata': {}
    }

    return user


def user_pusher_to_sendbird():
    users = []
    with open(os.path.join(INPUT_PUSHER_PATH, PUSHER_USER_FILENAME), 'rb') as infile:
        pushers = ijson.items(infile, 'item')
        path = os.path.join(OUTPUT_SENDBIRD_PATH, SENDBIRD_USER_FILENAME)
        for i, pusher in enumerate(pushers, 1):
            sendbird = init_user()
            try:
                sendbird['user_id'] = pusher['id']
                sendbird['nickname'] = pusher['name']
            except KeyError as ke:
                print('{0}\n{1}'.format(pusher, ke))
                return False
            if 'avatar_url' in pusher:
                sendbird['profile_url'] = pusher['avatar_url']
            if 'custom_data' in pusher:
                sendbird['metadata'] = pusher['custom_data']
            # TODO: if you have users' profile images, you can save the name as UUID.
            # if 'profile_file' in pusher:
            #   sendbird['profile_file'] = `{UUID}.{ext}` - you can use uuid.uuid4()
            # No pusher['created_at'] and pusher['updated_at']
            users.append(sendbird)
            if (i % USERS_PER_FILE == 0):
                with open('{0}{1}.json'.format(path, i//USERS_PER_FILE), 'w') as outfile:
                    json.dump(users, outfile)
                    users = []
        with open('{0}{1}.json'.format(path, (i//USERS_PER_FILE)+1), 'w') as outfile:
            json.dump(users, outfile)
    return True


#######################################################
# MESSAGE
#######################################################
PUSHER_ROOM_FILENAME = 'rooms.json'  # input
PUSHER_MESSAGE_FILENAME = 'messages.json'  # input
CHANNELS_PER_FILE = 1000
SENDBIRD_MESSAGE_FILENAME = 'exported_sendbird_messages'  # output


def init_channel():
    channel = {
        "channel": {
            "channel_url": "",
            "is_distinct": True,
            "is_public": False,
            "name": "",
            "custom_type": "",
            "data": "",
            "created_at": 0,
            "cover_url": "",
            "members": []
        },
        "messages": []
    }
    return channel


def init_message():
    message = {
        "user_id": "",
        "type": "MESG",
        "custom_type": "",
        "data": "",
        "dedup_id": "",
        "ts": 0
    }
    return message


def message_pusher_to_sendbird():
    channels = {}
    with open(os.path.join(INPUT_PUSHER_PATH, PUSHER_ROOM_FILENAME), 'rb') as infileroom:
        pushers = ijson.items(infileroom, 'item')
        for pusher in pushers:
            sendbird = init_channel()
            try:
                sendbird['channel']['channel_url'] = pusher['id']
                sendbird['channel']['name'] = pusher['name']
                for member_id in pusher['member_ids']:
                    sendbird['channel']['members'].append(
                        {'user_id': member_id})
                sendbird['channel']['is_public'] = not pusher['private']
                if 'custom_data' in pusher:
                    sendbird['channel']['data'] = pusher['custom_data']
                sendbird['channel']['created_at'] = int(
                    parse(pusher['created_at']).timestamp())

                channels[pusher['id']] = sendbird
            except KeyError as ke:
                print('{0}\n{1}'.format(pusher, ke))
                return False

    with open(os.path.join(INPUT_PUSHER_PATH, PUSHER_MESSAGE_FILENAME), 'rb') as infilemsg:
        pushers = ijson.items(infilemsg, 'item')
        for pusher in pushers:
            sendbird = init_message()
            try:
                sendbird['dedup_id'] = pusher['id']
                sendbird['user_id'] = pusher['sender_id']
                sendbird['ts'] = int(
                    parse(pusher['created_at']).timestamp()) * 1000

                parts = pusher['parts']
                if len(parts) == 1 and parts[0]['part_type'] == 'inline':
                    sendbird['message'] = parts[0]['payload']['content']
                else:
                    sendbird['type'] = 'FILE'
                    sendbird['data'] = {}
                    for part in parts:
                        if part['part_type'] == 'inline':
                            sendbird['data']['message'] = part['payload']['content']
                        if part['part_type'] == 'url':
                            sendbird['data']['type'] = part['payload']['type']
                            sendbird['data']['url'] = part['payload']['url']
                        if part['part_type'] == 'attachment':
                            sendbird['file_type'] = part['payload']['type']
                            # after downloading using pusher API, you have to change the file_name to `{UUID}.{ext}`.
                            sendbird['file_name'] = part['payload']['name']
                            sendbird['file_size'] = part['payload']['size']
                            sendbird['url'] = part['payload']['download_url']
                            sendbird['data']['custom_data'] = part['payload']['custom_data']
                channels[pusher['room_id']]['messages'].append(sendbird)
            except KeyError as ke:
                print('{0}\n{1}'.format(pusher, ke))
                return False
    pre = 0
    channels = list(channels.values())
    path = os.path.join(OUTPUT_SENDBIRD_PATH, SENDBIRD_MESSAGE_FILENAME)
    for i in range(1, len(channels)):
        if (i % CHANNELS_PER_FILE == 0):
            with open('{0}{1}.json'.format(path, i//CHANNELS_PER_FILE), 'w') as outfile:
                json.dump(channels[pre:i], outfile)
                pre = i
    with open('{0}{1}.json'.format(path, (i//CHANNELS_PER_FILE)+1), 'w') as outfile:
        json.dump(channels[pre:], outfile)

    return True


if __name__ == '__main__':
    assert user_pusher_to_sendbird() is True  # exported_sendbird_usersX.json
    assert message_pusher_to_sendbird() is True  # exported_sendbird_messagesX.json
