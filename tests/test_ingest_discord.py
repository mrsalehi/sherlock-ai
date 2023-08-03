import yaml
import pytest
from argparse import ArgumentParser, Namespace

from sherlock.utils import (
    read_config_from_yaml, 
    dict_to_namespace, 
    override_config_with_parsed_args,
)
from sherlock.ingestion.discord.read_discord import DiscordChannelConnector

@pytest.mark.parametrize("config_fpath", ["tests/data/test_discord_config.yaml"])
def test_read_discord(config_fpath):
    discord_connector = DiscordChannelConnector(config_fpath)
    messages = discord_connector.get_messages()
    print(messages)