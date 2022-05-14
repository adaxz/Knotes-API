from kobo_db.model import Bookmark, Content
from parsers.knotes_parser import KnoteParser
from parsers.models import Note, KoboNotePosition
from kobo_db.db import ContentTable, BookmarkTable
import bisect


class KoboNotesParser(KnoteParser):
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.content_table = ContentTable(filename)
        self.bookmark_table = BookmarkTable(filename)

    def get_notes_by_bookname(self, bookname: str) -> list[Note]:
        result = []
        content = self.content_table.select_content_by_book_title(bookname)
        if content:
            volume_id = content.BookID
            bookmarks = self.bookmark_table.select_marks_by_volume_id(
                volume_id)
            for bookmark in bookmarks:
                note = self._parse_note(bookmark, content)
                result.append(note)

        return result

    def _get_bookmark_position(self, bookmark: Bookmark) -> KoboNotePosition:
        all_contents = self.content_table.select_contents_by_book_id(
            bookmark.VolumeID)
        content = self.content_table.select_content_mark_by_content_id(
            bookmark.ContentID)
        try:
            chapter_name = self._form_chapter_name(
                all_contents, bookmark, content.Title)
        except:
            chapter_name = content.BookTitle
        percentage = round(bookmark.ChapterProgress, 4)

        return KoboNotePosition(chapter_name, percentage)

    def _form_chapter_name(self, all_contents: list[Content], bookmark: Bookmark, chapter_name: str) -> str:
        content = self.content_table.select_content_mark_by_content_id(
            bookmark.ContentID)

        content_level = int(content.ContentID[-1])

        if content_level == 1:
            return chapter_name
        else:
            upper_level_contents = sorted(
                [c for c in all_contents if c.ContentID[-1] == str(content_level-1)], key=lambda c: c.VolumeIndex)
            upper_level_volume_ix = sorted(
                [c.VolumeIndex for c in upper_level_contents])
            nearest_upper_level_idx = bisect.bisect(
                upper_level_volume_ix, content.VolumeIndex)
            nearest_upper_level_content = upper_level_contents[nearest_upper_level_idx-1]
            chapter_name = f'{nearest_upper_level_content.Title} ' + \
                chapter_name
            return self._form_chapter_name(
                all_contents, nearest_upper_level_content, chapter_name)

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
        all_contents = self.content_table.select_all_contents()
        all_books = list(set([content.BookTitle for content in all_contents]))
        all_books = list(filter(lambda x: x != '' and x != None, all_books))
        return all_books
