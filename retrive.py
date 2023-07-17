import cohere
from datasets import load_dataset
import tqdm

co = cohere.Client("v42IeRmnJ3hvf0hRZQrc8uSMOXExXDLotSxPsr7J")

# Get your cohere API key on: www.cohere.com
# def retrieve_top_docs(query, text_docs):
def cohere_rerank_retrieve_top_k(query, text_docs, top_k=1):
    """
    query: a simple string 
    text_docs: a list of strings where each one is a doc
    """
    # Example query and passages
    results = co.rerank(query=query, documents=text_docs, top_n=top_k, model="rerank-multilingual-v2.0")

    return results