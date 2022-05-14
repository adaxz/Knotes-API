from dataclasses import dataclass
from enum import Enum


@dataclass
class Note:
    bookname: str
    position: str
    time: str
    content: str


@dataclass
class KoboNotePosition:
    chapter_name: str
    chapter_progress: float

    def __repr__(self) -> str:
        percentage = round(self.chapter_progress * 100, 2)
        return f'Chapter 「{self.chapter_name}」at {percentage}%'


class NotionBlock:
    def __init__(self, type: str, content: str) -> None:
        self.block = {
            'object': 'block',
            'type': type,
            type: {
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                                'content': content,
                        },
                    },
                ],
            },
        }


class DeviceType(Enum):
    KINDLE = 'kindle'
    KOBO = 'kobo'

    @classmethod
    def to_list(cls) -> list[str]:
        return [e.value for e in cls]
