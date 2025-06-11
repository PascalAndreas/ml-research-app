from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine

from .file_watcher import start_watcher
from .routes import paper_router, tag_router

DATABASE_URL = "sqlite:///papers.db"
engine = create_engine(DATABASE_URL, echo=False)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["tauri://localhost"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLModel.metadata.create_all(engine)

start_watcher(engine)

app.include_router(paper_router)
app.include_router(tag_router)
