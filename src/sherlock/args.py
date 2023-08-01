from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--query", type=str, default="How does Instructor embedding work?")

    group = parser.add_argument_group("discord")
    group.add_argument("--discord.enable", action="store_true", default=False)
    group.add_argument("--discord.channel", type=str)
    group.add_argument("--discord.token", type=str)

    group = parser.add_argument_group("notebook")
    group.add_argument("--notebook.enable", action="store_true", default=False)
    group.add_argument("--notebook.path", type=str, default="examples/docs/llama_index", help="path to the notebook files dir. For now just local files. Maybe add support for remote files later??")

    # NOTE: Please read the docstring of the generate_response function in llm_generate_response.py for more details on the following argument
    group = parser.add_argument_group("llm")
    parser.add_argument("--llm.context_mode", type=str, default="all_in_one_context", choices=["all_in_one_context", "separate_context"])

    group = parser.add_argument_group("rerank")
    parser.add_argument("--rerank.model_name", type=str, default="cohere_rerank")
    parser.add_argument("--rerank.enable", action="store_true", default=False, help="use Cohere Rerank to retrieve top k docs")
    parser.add_argument("--rerank.top_k", type=int, default=1, help="top k docs to retrieve using Rerank. Note that we retrieve the documents of each knowledge source separately.")

    group = parser.add_argument_group("markdown")  # search in markdown docs
    group.add_argument("--markdown.enable", action="store_true", default=False)
    group.add_argument("--markdown.path", type=str, default="examples/docs/llama_index", help="path to the markdown docs dir. For now just local files. Maybe add support for remote files later??")

    group = parser.add_argument_group("vector_index")
    group.add_argument("--vector_index.enable", action="store_true", default=False)
    group.add_argument("--vector_index.name", type=str, default="pinecone", choices=["pinecone", "weaviate"])

    group = parser.add_argument_group("embeddings")
    group.add_argument("--embeddings.enable", action="store_true", default=False)
    group.add_argument("--embeddings.model_name", type=str, default="text-embedding-ada-002", help="model name of the sentence transformer model to use for generating embeddings")

    args = parser.parse_args()

    return args
