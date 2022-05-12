from sqlalchemy import Column, Text, REAL
from sqlalchemy.ext.declarative import declarative_base

_base = declarative_base()


class Bookmark(_base):
    __tablename__ = "Bookmark"

    BookmarkID = Column(Text, primary_key=True)
    DateCreated = Column(Text)
    ContentID = Column(Text)
    VolumeID = Column(Text)
    Text = Column(Text)
    ChapterProgress = Column(REAL)

    def __repr__(self) -> str:
        return f"Bookmark(ContentID={self.ContentID}, BookmarkID={self.BookmarkID})"


class Content(_base):
    __tablename__ = "content"

    ContentID = Column(Text, primary_key=True)
    ContentType = Column(Text)
    BookID = Column(Text)
    BookTitle = Column(Text)
    Title = Column(Text)

    def __repr__(self) -> str:
        return f"Content(BookTitle={self.BookTitle}, ContentID={self.ContentID})"
