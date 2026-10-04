import json
import os
import boto3
import yaml
from fastembed import SparseTextEmbedding
from qdrant_client import QdrantClient
CFG = yaml.safe_load(open("config/rag.yaml"))
MODEL_CACHE = os.environ.get("MODEL_CACHE", "./models")
COLLECTION = "kb"
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
qdrant = QdrantClient(url=os.environ.get("QDRANT_URL", CFG["qdrant_url"]))
bm25 = SparseTextEmbedding("Qdrant/bm25", cache_dir=MODEL_CACHE)
def embed(text: str) -> list[float]:
 body = json.dumps({"inputText": text, "dimensions": 1024, "normalize": True})
 resp = bedrock.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=body)
 return json.loads(resp["body"].read())["embedding"]