from kobo_db.model import Bookmark, Content
from parsers.knotes_parser import KnoteParser
from parsers.models import Note, KoboNotePosition
from kobo_db.db import Database


class KoboNotesParser(KnoteParser):
    def __init__(self, filename) -> None:
        super().__init__(filename)

    def get_notes_by_bookname(self, bookname: str) -> list[Note]:
        result = []
        content = Database.ContentTable.select_content_by_book_title(bookname)
        if content:
            content_id = content.ContentID
            bookmarks = Database.BookmarkTable.select_marks_by_contentID(
                content_id)
            for bookmark in bookmarks:
                note = self._parse_note(bookmark, content)
                result.append(note)

        return result

    def _get_bookmark_position(self, bookmark: Bookmark) -> KoboNotePosition:
        content = Database.ContentTable.select_content_by_content_id(
            bookmark.ContentID+'-1')
        chapter_name = content.Title
        percentage = round(bookmark.ChapterProgress, 4)

        return KoboNotePosition(chapter_name, percentage)

    def _parse_note(self, bookmark: Bookmark, content: Content) -> Note:
        position = str(self._get_bookmark_position(bookmark))

        note = Note(
            bookname=content.BookTitle,
            position=position,
            time=bookmark.DateCreated,
            content=bookmark.Text
        )

        return note

    def get_all_books(self) -> list[str]:
        all_contents = Database.ContentTable.select_all_contents()
        all_books = list(set([content.BookTitle for content in all_contents]))
        return all_books
