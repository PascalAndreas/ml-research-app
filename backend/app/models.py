from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship


class PaperTagLink(SQLModel, table=True):
    paper_id: str = Field(foreign_key="paper.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class Paper(SQLModel, table=True):
    id: str = Field(primary_key=True)
    filename: str
    title: Optional[str] = None
    authors: Optional[str] = None
    abstract: Optional[str] = None
    year: Optional[int] = None
    date_added: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: Optional[datetime] = None

    tags: List["Tag"] = Relationship(back_populates="papers", link_model=PaperTagLink)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    hue: int

    papers: List[Paper] = Relationship(back_populates="tags", link_model=PaperTagLink)
