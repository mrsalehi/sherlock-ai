
import logging
from argparse import ArgumentParser
from collections import defaultdict

from datasets import load_dataset

from sherlock.rerank.cohere_rerank import cohere_rerank_retrieve_top_k
from sherlock.llm.llm_utils import generate_response
from sherlock.ingestion.markdown.read_md_doc import read_md_docs
from sherlock.ingestion.discord.read_discord import DiscordConnector
from sherlock.ingestion.notebook.read_notebook import read_nbs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(args):
    query = args.query
    repo = args.repo    
    top_k = args.top_k

    context_docs = defaultdict(list)

    # NOTE: By default, we always support using the documentation to answer the query
    md_docs = read_md_docs(repo) # documentation docs
    top_md_docs = cohere_rerank_retrieve_top_k(query, md_docs, top_k=top_k)
    for el in top_md_docs:
        context_docs["MARKDOWN DOCUMENTS"].append(el.document['text'])

    if args.use_nb: 
        cells, md_cells, code_cells, md_id_to_cell_id, code_id_to_cell_id = read_nbs(repo) # returns markdown cells and code cells
        top_md_nbs = cohere_rerank_retrieve_top_k(query, md_cells, top_k=top_k)
        for el in top_md_nbs:
            md_cell_idx = el.index
            cell_idx = md_id_to_cell_id[md_cell_idx]
            # using the previous and next cells as context. Probably they are code cells??
            if cell_idx > 0: 
                context_docs["JUYPTER NOTEBOOKS"].append(cells[cell_idx-1])
            context_docs["JUYPTER NOTEBOOKS"].append(el.document['text'])
            if cell_idx < len(cells)-1:
                context_docs["JUYPTER NOTEBOOKS"].append(cells[cell_idx+1])
    
    if args.use_discord:
        discord_msgs = get_discord_messages(repo)
        top_discord_msgs = cohere_rerank_retrieve_top_k(query, discord_msgs, top_k=top_k)
        for el in top_discord_msgs:
            context_docs["DISCORD MESSAGES"].append(el.document['text'])

    # context_doc, context_discord, context_nb = [], [], []
    
    generate_response(
        query=query,
        context_docs=context_docs
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--repo", type=str, required=True)  # for now we only support langchain and llama index repos
    parser.add_argument("--use_discord", action="store_true", default=False, help="use discord messages to answer the query")
    parser.add_argument("--use_nb", action="store_true", default=False, help="use jupyter notebooks to answer the query")

    # NOTE: Please read the docstring of the generate_response function in llm_generate_response.py for more details on the following argument
    parser.add_argument("--llm_context_mode", type=str, default="all_in_one_context", choices=["all_in_one_context", "separate_context"])

    parser.add_argument("--use_rerank", action="store_true", default=False, help="use Cohere Rerank to retrieve top k docs")
    parser.add_argument("--top_k", type=int, default=1, help="top k docs to retrieve using Rerank. Note that we retrieve the documents of each knowledge source separately.")

    args = parser.parse_args()
    assert args.repo in ["langchain", "llama_index"]
    main(args=args)