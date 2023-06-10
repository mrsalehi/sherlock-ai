
from retrive_top_docs import retrieve_top_docs
from datasets import load_dataset
from llm_generate_response import generate_response
from read_docs import read_docs

def main():
    # query = "What is the capital of the United States?"
    query = "How can I create a chatbot and how can I add memory to it?"

    # # documents = [
    # #    "Carson City is the capital city of the American state of Nevada. At the  2010 United States Census, Carson City had a population of 55,274.",
    # #    "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean that are a political division controlled by the United States. Its capital is Saipan.",
    # #    "Charlotte Amalie is the capital and largest city of the United States Virgin Islands. It has about 20,000 people. The city is on the island of Saint Thomas.",
    # #    "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district. ",
    # #    "Capital punishment (the death penalty) has existed in the United States since before the United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.",
    # #    "North Dakota is a state in the United States. 672,591 people lived in North Dakota in the year 2010. The capital and seat of government is Bismarck."
    # #    ]
    
    data = load_dataset(f"Cohere/wikipedia-22-12", "simple", split='train', streaming=True)
    # # sample_data = data
    sample_data = []

    counter = 0
    for d in data:
        sample_data.append(d)
        counter += 1
        if counter == 1000:
            break

    # # all_docs =  map(lambda row : {"_index": index, "_id": row['id'], "_source": {"text": row['text']}}, data)
    # all_docs =  map(lambda row : {"_index": index, "_id": row['id'], "_source": {"text": row['text']}}, sample_data)

    # index = "wikipedia"

    # text_docs = []

    # for doc in all_docs:
    #     text_docs.append(doc['_source']['text'])

    text_docs = read_docs()
    
    res = retrieve_top_docs(query, text_docs)

    contexts = []
    for el in res:
        contexts.append(el.document['text'])

    generate_response(query=query, documents=contexts)


if __name__ == "__main__":
    main()
    