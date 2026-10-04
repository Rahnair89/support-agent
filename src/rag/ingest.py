import pathlib
import uuid

from qdrant_client import models

from rag.common import CFG, COLLECTION, bm25, embed, qdrant


def chunks(text, size, overlap):
    return [text[i:i + size] for i in range(0, len(text), size - overlap)]


def main():
    if qdrant.collection_exists(COLLECTION):
        qdrant.delete_collection(COLLECTION)
    qdrant.create_collection(
        COLLECTION,
        vectors_config={"dense": models.VectorParams(size=1024, distance=models.Distance.COSINE)},
        sparse_vectors_config={"sparse": models.SparseVectorParams(modifier=models.Modifier.IDF)},
    )
    points = []
    for path in sorted(pathlib.Path("kb").glob("*.md")):
        for chunk in chunks(path.read_text(), CFG["chunk_size"], CFG["chunk_overlap"]):
            sparse = next(bm25.embed([chunk]))
            points.append(models.PointStruct(
                id=str(uuid.uuid4()),
                vector={
                    "dense": embed(chunk),
                    "sparse": models.SparseVector(indices=sparse.indices.tolist(),
                                                  values=sparse.values.tolist()),
                },
                payload={"source": path.name, "text": chunk},
            ))
    qdrant.upsert(COLLECTION, points)
    print(f"Ingested {len(points)} chunks")


if __name__ == "__main__":
    main()
