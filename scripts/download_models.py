import os

from fastembed import SparseTextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder

cache = os.environ.get("MODEL_CACHE", "./models")
SparseTextEmbedding("Qdrant/bm25", cache_dir=cache)
TextCrossEncoder("Xenova/ms-marco-MiniLM-L-6-v2", cache_dir=cache)
print("models cached in", cache)
