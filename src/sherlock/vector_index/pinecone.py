import pinecone
from typing import List, Union

# connect to pinecone environment
pinecone.init(
    api_key="API_KEY_HERE",
    environment="us-central1-gcp"  # find next to API key in console
)


class PineconeIndex:
    def __init__(self, index_name: str, embedding_dim: int = 768):
        self.index_name = index_name
        # check if the abstractive-question-answering index exists
        if index_name not in pinecone.list_indexes():
            # create the index if it does not exist
            pinecone.create_index(
                index_name,
                dimension=embedding_dim,
                metric="cosine"
            )

        self.index = pinecone.Index(index_name)
    
    def add_embeddings(self, embeds, ids=None, texts=None):
        if ids is None:
            ids = list(range(len(embeds))) 
        meta = [{"text": text} for text in texts] if texts is not None else {}
        # to_upsert = zip(*[v for v in [ids, embeds, meta] if v is not None])
        to_upsert = zip(ids, embeds, meta)
        self.index.upsert(items=to_upsert)
    
    def query_index(self, query: str, top_k: int = 10, include_metadata: bool = True):
        res = self.index.query(queries=[query], top_k=top_k, include_metadata=include_metadata)

        return res