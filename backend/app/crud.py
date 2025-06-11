from typing import Optional, List
from sqlmodel import Session, select
from .models import Paper, Tag, PaperTagLink


def get_paper(session: Session, paper_id: str) -> Optional[Paper]:
    return session.get(Paper, paper_id)


def list_papers(
    session: Session,
    *,
    tag: Optional[int] = None,
    query: Optional[str] = None,
    sort: Optional[str] = None,
) -> List[Paper]:
    """Return list of papers filtered and sorted."""

    statement = select(Paper)

    if tag is not None:
        statement = statement.join(PaperTagLink).where(PaperTagLink.tag_id == tag)

    if query:
        like = f"%{query}%"
        statement = statement.where(
            Paper.title.ilike(like) | Paper.authors.ilike(like)
        )

    if sort == "access":
        statement = statement.order_by(Paper.last_accessed.desc())
    elif sort == "added":
        statement = statement.order_by(Paper.date_added.desc())

    return session.exec(statement).all()


def create_tag(session: Session, name: str, hue: int) -> Tag:
    tag = Tag(name=name, hue=hue)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag
