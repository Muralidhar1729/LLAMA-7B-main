from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from .config import QDRANT_URL, QDRANT_API_KEY

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def ensure_collection(name: str, vector_size: int, distance: str = "COSINE"):
    dist = getattr(qmodels.Distance, distance)  # This is now corrected
    if not client.collection_exists(name):
        client.create_collection(
            collection_name=name,
            vectors_config=qmodels.VectorParams(size=vector_size, distance=dist)
        )

def upsert_points(collection: str, vectors, payloads, ids=None):
    from uuid import uuid4
    ids = ids or [str(uuid4()) for _ in range(len(vectors))]
    points = [
        qmodels.PointStruct(id=id_, vector=vec, payload=payload)
        for id_, vec, payload in zip(ids, vectors, payloads)
    ]
    client.upsert(collection_name=collection, points=points)
    return ids

def search(collection: str, vector, top_k: int = 5, filters=None):
    return client.search(
        collection_name=collection,
        query_vector=vector,
        limit=top_k,
        query_filter=filters
    )
