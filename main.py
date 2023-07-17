
from retrive import cohere_rerank_retrieve_top_k
from datasets import load_dataset
from llm_utils import generate_response
from read_md_doc import read_md_docs
import json
from argparse import ArgumentParser
from read_discord import get_discord_messages
from read_notebook import read_nbs
from collections import defaultdict


def main(args):
    # query = "What is the capital of the United States?"
    # query = "How can I create a chatbot and how can I add memory to it?"
    # query = "FAISS.from_documents(docs, embedding) is so slow. Has anyone faced it before?"

    # # documents = [
    # #    "Carson City is the capital city of the American state of Nevada. At the  2010 United States Census, Carson City had a population of 55,274.",
    # #    "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean that are a political division controlled by the United States. Its capital is Saipan.",
    # #    "Charlotte Amalie is the capital and largest city of the United States Virgin Islands. It has about 20,000 people. The city is on the island of Saint Thomas.",
    # #    "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district. ",
    # #    "Capital punishment (the death penalty) has existed in the United States since before the United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.",
    # #    "North Dakota is a state in the United States. 672,591 people lived in North Dakota in the year 2010. The capital and seat of government is Bismarck."
    # #    ]
    
    # data = load_dataset(f"Cohere/wikipedia-22-12", "simple", split='train', streaming=True)
    # # # sample_data = data
    # sample_data = []

    # counter = 0
    # for d in data:
    #     sample_data.append(d)
    #     counter += 1
    #     if counter == 1000:
    #         break

    # # all_docs =  map(lambda row : {"_index": index, "_id": row['id'], "_source": {"text": row['text']}}, data)
    # all_docs =  map(lambda row : {"_index": index, "_id": row['id'], "_source": {"text": row['text']}}, sample_data)

    # index = "wikipedia"

    # text_docs = []

    # for doc in all_docs:
    #     text_docs.append(doc['_source']['text'])
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
        md_cells, code_cells, md_id_to_cell_id, code_id_to_cell_id = read_nbs(repo) # returns markdown cells and code cells
        top_md_nbs = cohere_rerank_retrieve_top_k(query, md_cells, top_k=top_k)
        # QUESTION: can we find which markdown cell id was retrieved?
        for el in top_md_nbs:
            context_docs["JUYPTER NOTEBOOKS"].append(el.document['text'])
    
    if args.use_discord:
        discord_msgs = get_discord_messages(repo)
        top_discord_msgs = cohere_rerank_retrieve_top_k(query, discord_msgs, top_k=top_k)
        for el in top_discord_msgs:
            context_docs["DISCORD MESSAGES"].append(el.document['text'])

    # context_doc, context_discord, context_nb = [], [], []
    
    generate_response(
        query=query, 
        context_docs=context_docs,
        # documents_doc=context_doc, 
        # documents_discord=context_discord,
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