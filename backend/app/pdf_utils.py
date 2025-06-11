import hashlib
from pathlib import Path
import fitz


def pdf_sha1(path: Path) -> str:
    with open(path, 'rb') as f:
        data = f.read()
    return hashlib.sha1(data).hexdigest()


def extract_metadata(path: Path) -> dict:
    doc = fitz.open(path)
    meta = doc.metadata or {}
    return {
        'title': meta.get('title'),
        'authors': meta.get('author'),
        'abstract': None,
        'year': int(meta.get('creationDate', '')[2:6] or 0) if meta.get('creationDate') else None,
    }
