from sentence_transformers import SentenceTransformer
from .config import EMBED_MODEL_NAME, TOP_K, CHUNK_SIZE, CHUNK_OVERLAP
from .store import ensure_collection, upsert_points, search
from .llm_client import chat
from .ingest import read_text, chunk_text

embedder = SentenceTransformer(EMBED_MODEL_NAME)
EMBED_DIM = embedder.get_sentence_embedding_dimension()

def collection_name(tenant_id: str) -> str:
    return f"docs_{tenant_id}_{EMBED_DIM}"

def embed_texts(texts):
    return embedder.encode(texts, normalize_embeddings=True).tolist()

def ingest_paths(tenant_id: str, paths):
    collection = collection_name(tenant_id)
    ensure_collection(collection, EMBED_DIM)

    payloads, chunks = [], []
    for path in paths:
        text = read_text(path)
        cks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        chunks.extend(cks)
        payloads.extend([{"source": path, "text": ck} for ck in cks])

    vectors = embed_texts([p["text"] for p in payloads])
    upsert_points(collection, vectors, payloads)
    return {"chunks": len(chunks), "collection": collection}

def retrieve(tenant_id: str, question: str, top_k: int = TOP_K):
    collection = collection_name(tenant_id)
    q_vec = embed_texts([question])[0]
    results = search(collection, q_vec, top_k=top_k)
    contexts = []
    for r in results:
        payload = r.payload or {}
        contexts.append({
            "text": payload.get("text", ""),
            "source": payload.get("source", ""),
            "score": r.score
        })
    return contexts

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer strictly using the provided context. "
    "If the answer is not in the context, say you don't know."
)

def answer(tenant_id: str, question: str):
    contexts = retrieve(tenant_id, question)
    context_block = "\n\n".join(
        f"[{i+1}] {c['text']}\n(Source: {c['source']})" for i, c in enumerate(contexts)
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",
         "content": f"Context:\n{context_block}\n\nQuestion: {question}\n\n"
                    f"Respond concisely and cite sources like [1], [2] if used."}
    ]
    content = chat(messages)
    sources = [{"source": c["source"], "rank": i+1, "score": c["score"]} for i, c in enumerate(contexts)]
    return {"answer": content, "sources": sources}
