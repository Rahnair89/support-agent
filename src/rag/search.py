from fastembed.rerank.cross_encoder import TextCrossEncoder
from qdrant_client import models

from rag.common import COLLECTION, MODEL_CACHE, bm25, embed, qdrant

reranker = TextCrossEncoder("Xenova/ms-marco-MiniLM-L-6-v2", cache_dir=MODEL_CACHE)


def hybrid_search(query: str, cfg: dict) -> list[dict]:
    qs = next(bm25.query_embed(query))
    hits = qdrant.query_points(
        COLLECTION,
        prefetch=[
            models.Prefetch(query=embed(query), using="dense", limit=cfg["candidates"]),
            models.Prefetch(
                query=models.SparseVector(indices=qs.indices.tolist(), values=qs.values.tolist()),
                using="sparse", limit=cfg["candidates"]),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=cfg["candidates"],
    ).points
    if not hits:
        return []
    scores = list(reranker.rerank(query, [h.payload["text"] for h in hits]))
    ranked = sorted(zip(scores, hits), key=lambda x: x[0], reverse=True)[: cfg["top_k"]]
    return [{"source": h.payload["source"], "text": h.payload["text"], "score": float(s)}
            for s, h in ranked]
