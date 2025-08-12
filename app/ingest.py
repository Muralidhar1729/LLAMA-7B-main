import os, glob, re
from pypdf import PdfReader

def read_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in [".txt", ".md", ".py", ".log"]:
        return open(path, "r", errors="ignore").read()
    if ext == ".pdf":
        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    raise ValueError(f"Unsupported file type: {ext}")

def chunk_text(text: str, chunk_size=400, overlap=50):
    text = re.sub(r"\s+", " ", text).strip()
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        cut = text.rfind(".", start, end)
        if cut == -1 or (cut - start) < chunk_size * 0.5:
            cut = end
        else:
            cut += 1
        chunks.append(text[start:cut].strip())
        start = max(0, cut - overlap)
    return chunks
