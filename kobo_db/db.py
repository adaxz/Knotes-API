from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
from kobo_db.model import Bookmark, Content


DB_CONNECT_STR = 'sqlite:///' + config.KOBO_DB_DIR

_engine = create_engine(DB_CONNECT_STR)
_session = sessionmaker(bind=_engine)


class Database:
    class BookmarkTable:
        def select_marks_by_contentID(contentID: str) -> list[Bookmark]:
            contentID = contentID.split('!')[0]
            return _session().query(Bookmark).filter(Bookmark.ContentID.contains(contentID)).order_by(Bookmark.DateCreated).all()

    class ContentTable:
        def select_content_by_book_title(book_title: str) -> Content:
            return _session().query(Content).filter(Content.BookTitle == book_title).first()

        def select_all_contents() -> list[Content]:
            return _session().query(Content).all()

        def select_content_by_content_id(content_id: str) -> Content:
            return _session().query(Content).filter(Content.ContentID == content_id).first()
