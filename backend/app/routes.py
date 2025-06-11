from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from .models import Paper, Tag, PaperTagLink
from .crud import create_tag, list_papers as crud_list_papers

router = APIRouter()


def get_session():
    from .main import engine
    with Session(engine) as session:
        yield session


paper_router = APIRouter(prefix="/papers")

tag_router = APIRouter(prefix="/tags")


@paper_router.get("/")
async def list_papers(
    sort: str | None = None,
    session: Session = Depends(get_session),
) -> List[Paper]:
    return crud_list_papers(session, sort=sort)


@paper_router.get("/{paper_id}")
async def get_paper(paper_id: str, session: Session = Depends(get_session)) -> Paper:
    paper = session.get(Paper, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@paper_router.get("/{paper_id}/pdf")
async def get_paper_pdf(paper_id: str, session: Session = Depends(get_session)):
    from .main import PDF_FOLDER
    paper = session.get(Paper, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    file_path = PDF_FOLDER / paper.filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="PDF file missing")
    return FileResponse(file_path)


@tag_router.get("/")
async def list_tags(session: Session = Depends(get_session)) -> List[Tag]:
    return session.exec(select(Tag)).all()


@tag_router.post("/")
async def create_new_tag(name: str, hue: int, session: Session = Depends(get_session)) -> Tag:
    return create_tag(session, name=name, hue=hue)
