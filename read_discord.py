import json


def get_discord_messages():
    with open("../get-discord-messages/messages3.json") as f:
        messages = json.load(f)  

    message_docs = messages
    # for message in messages:
        # message_docs.append(message['content'])
        # print(message['content'])
        # print("\n\n")
    return message_docs