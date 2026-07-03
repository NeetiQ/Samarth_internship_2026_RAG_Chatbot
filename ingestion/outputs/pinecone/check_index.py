from pinecone import Pinecone
from embedding_config import *

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

print(index.describe_index_stats())