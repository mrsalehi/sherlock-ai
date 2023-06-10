
from retrive_top_docs import retrieve_top_docs
from datasets import load_dataset
from llm_generate_response import generate_response
from read_docs import read_docs
import json
from argparse import ArgumentParser



def get_discord_messages():
    with open("../get-discord-messages/messages.json") as f:
        messages = json.load(f)  

    message_docs = []
    for message in messages:
        message_docs.append(message['content'])
        # print(message['content'])
        # print("\n\n")

    return message_docs


def main(query):
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

    documentation_docs = read_docs() # documentation docs
    discord_message_docs = get_discord_messages()

    # all_docs = text_docs + discord_message_docs
    # all_docs = text_docs

    res_documentation = retrieve_top_docs(query, documentation_docs)
    res_discord = retrieve_top_docs(query, discord_message_docs)

    context_doc, context_discord = [], []
    for el in res_documentation:
        context_doc.append(el.document['text'])
    
    for el in res_discord:
        context_discord.append(el.document['text'])

    generate_response(query=query, documents_doc=context_doc, documents_discord=context_discord)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--query", type=str, required=True)

    args = parser.parse_args()
    query = args.query
    main(query=query)
    