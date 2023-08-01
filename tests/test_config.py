import yaml
import pytest
from argparse import ArgumentParser, Namespace

from sherlock.utils import (
    read_config_from_yaml, 
    dict_to_namespace, 
    override_config_with_parsed_args,
)

@pytest.mark.parametrize("file_path", ["tests/data/test.yaml"])
def test_read_config_from_yaml(file_path):
    config = read_config_from_yaml(file_path)
    assert config['discord']['channel'] == 123
    assert config['rerank']['enable'] == True
    assert config['embeddings']['enable'] == False
    assert config['llm']['llama']['context_length'] == 1024


def test_dict_to_namespace():
    config = read_config_from_yaml("tests/data/test.yaml")
    config = dict_to_namespace(config)
    assert config.discord.channel == 123
    assert config.llm.llama.context_length == 1024
    assert config.rerank.enable == True
    assert config.embeddings.enable == False
    assert config.notebook.path == "examples/docs/llama_index"


def test_override_config_with_parsed_args():
    config = read_config_from_yaml("tests/data/test.yaml")

    args = {
        "query": "Test args query?",
        "discord.enable": False,
        "discord.channel": 8761234,
        "discord.token": "args_token",
        "llm.llama.context_length": 4096,
        "markdown.path": "examples/docs/langchain",
        "embeddings.model": "args_model"
    }

    args = Namespace(**args)
    
 
    assert config['query'] == "How does Instructor embedding work?"
    assert config['discord']['enable'] == True
    assert config['discord']['channel'] == 123
    assert config['discord']['token'] == "abc"
    assert config['llm']['llama']['context_length'] == 1024
    assert config['markdown']['path'] == "examples/docs/llama_index"
    assert config['embeddings']['model'] == "text-embedding-ada-002"

    config = override_config_with_parsed_args(config, args)

    assert config.query == "Test args query?"
    assert config.discord.enable == False
    assert config.discord.channel == 8761234 
    assert config.discord.token == "args_token"
    assert config.llm.llama.context_length == 4096
    assert config.markdown.path == "examples/docs/langchain"
    assert config.embeddings.model == "args_model"
