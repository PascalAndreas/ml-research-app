import asyncio
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlmodel import Session
from .models import Paper
import hashlib
import fitz


class PDFHandler(FileSystemEventHandler):
    def __init__(self, folder: Path, engine):
        self.folder = folder
        self.engine = engine

    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith('.pdf'):
            return
        path = Path(event.src_path)
        asyncio.create_task(self.process_file(path))

    async def process_file(self, path: Path):
        await asyncio.sleep(0.1)
        with open(path, 'rb') as f:
            sha1 = hashlib.sha1(f.read()).hexdigest()
        doc = fitz.open(path)
        meta = doc.metadata or {}
        paper = Paper(
            id=sha1,
            filename=path.name,
            title=meta.get('title'),
            authors=meta.get('author'),
            year=int(meta.get('creationDate', '')[2:6] or 0) if meta.get('creationDate') else None,
        )
        with Session(self.engine) as session:
            existing = session.get(Paper, sha1)
            if existing:
                return
            session.add(paper)
            session.commit()


def start_watcher(engine, folder: Optional[str] = None):
    if folder is None:
        return
    path = Path(folder)
    handler = PDFHandler(path, engine)
    observer = Observer()
    observer.schedule(handler, path=str(path), recursive=False)
    observer.start()
