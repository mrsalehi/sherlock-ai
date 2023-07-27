"""
OpenAI Embedding API
"""
import openai
from typing import List

openai.api_key = "TEST_KEY"  # FIXME: put the key here later
# get API key from top-right dropdown on OpenAI website

openai.Engine.list()  # check we have authenticated



class OpenAIEmbeddingModel:
    def __init__(self, model_name: str) -> None:
        assert model_name in {"text-embedding-ada-002"}
        self.model_name = model_name

    def get_embedding(self, text: List[str]):
        ret = openai.Embedding.create(
            input = [text], 
            model=self.model_name)
        embeddings = [el['embedding'] for el in ret['data']]

        return embeddings