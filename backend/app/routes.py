from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .models import Paper, Tag, PaperTagLink
from .crud import create_tag

router = APIRouter()


def get_session():
    from .main import engine
    with Session(engine) as session:
        yield session


paper_router = APIRouter(prefix="/papers")

tag_router = APIRouter(prefix="/tags")


@paper_router.get("/")
async def list_papers(session: Session = Depends(get_session)) -> List[Paper]:
    return session.exec(select(Paper)).all()


@paper_router.get("/{paper_id}")
async def get_paper(paper_id: str, session: Session = Depends(get_session)) -> Paper:
    paper = session.get(Paper, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@tag_router.get("/")
async def list_tags(session: Session = Depends(get_session)) -> List[Tag]:
    return session.exec(select(Tag)).all()


@tag_router.post("/")
async def create_new_tag(name: str, hue: int, session: Session = Depends(get_session)) -> Tag:
    return create_tag(session, name=name, hue=hue)
