from __future__ import annotations

from pathlib import Path
import sys

from sqlalchemy.orm import Session

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.db.models.knowledge_chunk import KnowledgeChunk
from app.db.session import SessionLocal


KNOWLEDGE_DIR = ROOT_DIR / "data" / "knowledge"


def _split_into_chunks(text: str, max_chars: int = 1000) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        if not current:
            current = para
        elif len(current) + 2 + len(para) <= max_chars:
            current += "\n\n" + para
        else:
            chunks.append(current)
            current = para

    if current:
        chunks.append(current)

    if not chunks and text.strip():
        return [text.strip()]
    return chunks


def _ingest_file(db: Session, path: Path) -> int:
    source_name = path.name
    if not path.is_file():
        return 0

    # очистим старые чанки для этого файла
    db.query(KnowledgeChunk).filter(KnowledgeChunk.source_name == source_name).delete(
        synchronize_session=False
    )

    content = path.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]
    title = next((line for line in lines if line), path.stem)

    chunks_text = _split_into_chunks(content, max_chars=1000)
    rows: list[KnowledgeChunk] = []
    for chunk_text in chunks_text:
        rows.append(
            KnowledgeChunk(
                source_name=source_name,
                title=title,
                content=chunk_text,
            )
        )

    if rows:
        db.add_all(rows)
    return len(rows)


def run() -> str:
    db = SessionLocal()
    try:
        if not KNOWLEDGE_DIR.exists():
            return f"Directory {KNOWLEDGE_DIR} not found"

        files = list(KNOWLEDGE_DIR.glob("*.txt")) + list(KNOWLEDGE_DIR.glob("*.md"))
        total_chunks = 0
        for path in files:
            total_chunks += _ingest_file(db, path)

        db.commit()
        return f"Ingested {total_chunks} chunks from {len(files)} files"
    finally:
        db.close()
