import json
import discord
from typing import List
from discord.ext import commands


def get_discord_messages():
    with open("../get-discord-messages/messages3.json") as f:
        messages = json.load(f)  

    message_docs = messages
    # for message in messages:
        # message_docs.append(message['content'])
        # print(message['content'])
        # print("\n\n")
    return message_docs


# self._create_full_tmp_dir_path()
# if self.config.verbose:
    # logger.debug(f"fetching {self} - PID: {os.getpid()}")
messages: List[discord.Message] = []
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)

@bot.event
async def on_ready():
    try:
        after_date = None

        channel = bot.get_channel(970731414494535703)
        async for msg in channel.history(after=after_date, limit=None):  # type: ignore
            messages.append(msg)

        print(messages[0])
        print(len(messages))
        await bot.close()
    except Exception as e:
        # logger.error(f"Error fetching messages: {e}")
        await bot.close()
        raise e

bot.run("MTExNzE1NzgyOTI5MjMzNTExNQ.GAm_WX.KCcahPTN-yiRWCkpONBNZJ4wwUr5N28jBX-Cac")