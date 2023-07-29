import json
import yaml
import discord
from typing import List
from discord.ext import commands
from datetime import datetime, timezone
import pytz

class DiscordConfig:
    def __init__(self) -> None:
        config = self._fetch_discord_config()

        try:
            self.token = config['token']
        except KeyError:
            raise KeyError("Missing token from Discord configuration")
        
        try:
            self.channelId = config['channelId']
        except KeyError:
            raise KeyError("Missing field channelId from Discord configuration")

    def _fetch_discord_config(self):
        try:
            with open("config.yaml", "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("No config.yaml file found containing discord configuration")        
        

class DiscordConnector:
    """
    Example usage:
    
        Discord = DiscordConnector()
        print(Discord.get_messages())
    """

    def __init__(self) -> None:
        self.config = DiscordConfig()
        self.messages: List[discord.Message] = []

        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix=">", intents=intents)

    def _get_current_timestamp(self):
        return datetime.now(timezone.utc).isoformat()

    def _get_timestamp_from_file(self):
        timestamp_file = f"{self.config.channelId}.json"
        try:
            with open(timestamp_file, "r") as file:
                dict = json.load(file)
                iso_timestamp_str = dict["lastFetch"]
                return datetime.fromisoformat(iso_timestamp_str)
        
        except FileNotFoundError:
            # Create a new file instead with the same timestamp
            self._rewrite_timestamp_file()
            return None
    
    def _delete_timestamp_file(self):
        pass

    def _rewrite_timestamp_file(self):
        timestamp_file = f"{self.config.channelId}.json"
        data = {"lastFetch": self._get_current_timestamp()}
        json_data = json.dumps(data, indent=4)
        
        with open(timestamp_file, "w") as file:
            file.write(json_data)

    def get_messages(self):
        @self.bot.event
        async def on_ready():
            try:
                timestamp = self._get_timestamp_from_file()
                after_date = timestamp

                print(f"Fetching all messages after {after_date}")

                channel = self.bot.get_channel(self.config.channelId)
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