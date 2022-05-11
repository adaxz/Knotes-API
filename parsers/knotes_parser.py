from abc import ABC, abstractmethod
from parsers.models import Note, NotionBlock


class KnoteParser(ABC):
    def __init__(self, filename='') -> None:
        self.filename = filename

    def note_to_notion_block(self, note: Note) -> list[dict]:
        content_block = NotionBlock('heading_1', note.content).block
        bookname_block = NotionBlock('bulleted_list_item', note.bookname).block
        position_blob = NotionBlock('bulleted_list_item', note.position).block
        time_blob = NotionBlock('bulleted_list_item', note.time).block

        return [content_block, bookname_block, position_blob, time_blob]

    def notes_to_page_content(self, notes: list[Note]) -> list[dict]:
        result = []
        for note in notes:
            result.extend(self.note_to_notion_block(note))

        return result

    @abstractmethod
    def get_all_books(self) -> list[str]:
        pass

    @abstractmethod
    def get_notes_by_bookname(self, bookname: str) -> list[Note]:
        pass
