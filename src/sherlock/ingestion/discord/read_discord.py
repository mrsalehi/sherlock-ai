import json
import yaml
import discord
from typing import List
from discord.ext import commands
from datetime import datetime, timezone
import os
import pytz
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscordChannelConfig:
    def __init__(self, config_path) -> None:
        self.config_path = config_path
        config = self._fetch_discord_config(config_path)

        try:
            self.token = config['token']
        except KeyError:
            raise KeyError("Missing token from Discord configuration")
        
        try:
            self.channel_id = config['channel_id']
        except KeyError:
            raise KeyError("Missing field channel_id from Discord configuration")

    def _fetch_discord_config(self, config_path):
        try:
            with open(config_path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("No config file found containing discord configuration")
        

class DiscordChannelConnector:
    """
    Example usage:
    
        Discord = DiscordConnector()
        print(Discord.get_messages())
    """

    def __init__(self, config_path: str) -> None:
        self.config = DiscordChannelConfig(config_path)
        self.messages: List[discord.Message] = []

        intents = discord.Intents.default()
        intents.message_content = True
        self.timestamp_fpath = f"data/{self.config.channel_id}.json"
        self.bot = commands.Bot(command_prefix=">", intents=intents)

    def _get_current_timestamp(self):
        return datetime.now(timezone.utc).isoformat()

    def _get_timestamp_from_file(self):
        try:
            with open(self.timestamp_file, "r") as file:
                dict = json.load(file)
                iso_timestamp_str = dict["last_fetch"]
                return datetime.fromisoformat(iso_timestamp_str)
        
        except FileNotFoundError:
            # Create a new file instead with the same timestamp
            self._rewrite_timestamp_file()
            return None
    
    def _delete_timestamp_file(self):
        logger.warning(f"Deleting timestamp file {self.timestamp_fpath}")
        os.remove(self.timestamp_fpath)

    def _rewrite_timestamp_file(self):
        data = {"last_fetch": self._get_current_timestamp()}
        json_data = json.dumps(data, indent=4)
        
        with open(self.timestamp_fpath, "w") as file:
            file.write(json_data)

    def get_messages(self):
        @self.bot.event
        async def on_ready():
            try:
                timestamp = self._get_timestamp_from_file()
                after_date = timestamp

                print(f"Fetching all messages after {after_date}")

                channel = self.bot.get_channel(self.config.channel_id)
                async for msg in channel.history(after=after_date, limit=None):
                    self.messages.append(msg.content)

                # Update the timestamp json to now when we succeed so we can fetch the new messages we haven't yet read
                self._rewrite_timestamp_file()

                # Exit this function by closing the bot
                await self.bot.close()

            except Exception as e:
                print("Received error: ", e)
                await self.bot.close()
                # If we fail, delete the timestamp file so we retry it for next time.
                self._delete_timestamp_file()
                raise e
        
        self.bot.run(self.config.token)
        return self.messages