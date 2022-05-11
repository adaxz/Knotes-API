import config
import os
import re
from parsers.models import Note
from parsers.knotes_parser import KnoteParser


class KindleNotesParser(KnoteParser):
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.notes = self._parse_all_notes()

    def _parse_all_notes(self) -> list[Note]:
        text = self._read_txt(self.filename)

        text_list = text.split('==========')
        text_list = [text for text in text_list if len(text.strip()) > 0]
        notes = [self._parse_one_note(note) for note in text_list]

        return notes

    def _read_txt(self, filename: str) -> str:
        fp = os.path.join(config.FIEL_DIR, filename)
        with open(fp, 'r') as txt_file:
            text = txt_file.read()

        return text

    def _parse_one_note(self, note: str) -> Note:
        note_split = re.split(r'\n|\n\n', note)
        note_split = [n.strip() for n in note_split if n != '']

        note_obj = Note(
            bookname=note_split[0],
            position=note_split[1].split('|')[0].strip(),
            time=note_split[1].split('|')[-1].strip(),
            content=note_split[-1])

        return note_obj

    def get_all_books(self) -> list[str]:
        names = [note.bookname for note in self.notes]
        return list(set(names))

    def get_notes_by_bookname(self, bookname: str) -> list[Note]:
        notes = [note for note in self.notes if note.bookname == bookname]

        return notes
