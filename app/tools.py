from __future__ import annotations

from pathlib import Path


def load_sops(corpus_dir: str | Path) -> list[dict[str, str]]:
    root = Path(corpus_dir)
    docs: list[dict[str, str]] = []
    if not root.exists():
        return docs
    for path in sorted(root.glob("*.md")):
        docs.append({"id": path.stem, "title": path.stem.replace("_", " "), "text": path.read_text(encoding="utf-8")})
    return docs


def search_sops(query: str, corpus_dir: str | Path, top_k: int = 3) -> list[dict[str, str]]:
    tokens = {t.lower() for t in query.replace("-", " ").split() if len(t) > 2}
    scored: list[tuple[int, dict[str, str]]] = []
    for doc in load_sops(corpus_dir):
        hay = (doc["title"] + " " + doc["text"]).lower()
        score = sum(1 for t in tokens if t in hay)
        if score:
            scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]
