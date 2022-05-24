from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
from kobo_db.model import Bookmark, Content, Word
import os
from abc import ABC


class DatabaseTable(ABC):
    def __init__(self, filename) -> None:
        self.DB_CONNECT_STR = 'sqlite:///' + \
            os.path.join(config.KOBO_FILE_DIR, filename)
        self._engine = create_engine(self.DB_CONNECT_STR)
        self._session = sessionmaker(bind=self._engine)


class BookmarkTable(DatabaseTable):
    def __init__(self, filename) -> None:
        super().__init__(filename)

    def select_marks_by_volume_id(self, volume_id: str) -> list[Bookmark]:
        return self._session().query(Bookmark).filter(Bookmark.VolumeID == volume_id).order_by(Bookmark.DateCreated).all()

    def select_marks_by_content_id(self, content_id: str) -> list[Bookmark]:
        return self._session().query(Bookmark).filter(Bookmark.ContentID == content_id).order_by(Bookmark.DateCreated).all()


class ContentTable(DatabaseTable):
    def __init__(self, filename) -> None:
        super().__init__(filename)

    def select_content_by_book_title(self, book_title: str) -> Content:
        return self._session().query(Content).filter(Content.BookTitle == book_title).first()

    def select_all_contents(self) -> list[Content]:
        return self._session().query(Content).all()

    def select_content_by_content_id(self, content_id: str) -> Content:
        return self._session().query(Content).filter(Content.ContentID == content_id).first()

    def select_content_mark_by_content_id(self, content_id: str) -> Content:
        return self._session().query(Content).filter(Content.ContentID.contains(content_id), Content.ContentType == 899).first()

    def select_contents_by_bookname(self, bookname: str) -> list[Content]:
        return self._session().query(Content).filter(Content.BookTitle == bookname).all()

    def select_contents_by_book_id(self, book_id: str) -> list[Content]:
        return self._session().query(Content).filter(Content.BookID == book_id).all()


class WordListTable(DatabaseTable):
    def __init__(self, filename) -> None:
        super().__init__(filename)

    def select_word_by_test(self, text: str) -> Word:
        return self._session().query(Word).filter(Word.Text == text).first()

    def select_words_by_volume_id(self, volume_id: str) -> list[Word]:
        return self._session().query(Word).filter(Word.VolumeId == volume_id).order_by(Word.DateCreated).all()
