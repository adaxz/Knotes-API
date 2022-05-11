from dataclasses import dataclass


@dataclass
class Note:
    bookname: str
    position: str
    time: str
    content: str


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
