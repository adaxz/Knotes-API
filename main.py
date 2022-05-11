from ast import parse
from parsers.kindle_parser import KindleNotesParser
from parsers.kobo_parser import KoboNotesParser
from senders.notion_sender import NotionApiActions

if __name__ == "__main__":
    filename = 'My Clippings.txt'

    bookname = "无缘社会(《穷忙族》NHK节目制作组原班人马新作，“人人自危、一起孤独”) (译文纪实) (NHK节目组)"
    page_name = '无缘社会'
    database_id = '03cd367b95a64ffea462c0b2bb67576c'

    parser = KindleNotesParser(filename)
    # print(parser.get_all_books())
    notes = parser.get_notes_by_bookname(bookname=bookname)
    notion_notes = parser.notes_to_page_content(notes)

    # parser = KoboNotesParser('')
    # print(parser.get_all_books())

    # notes = parser.get_notes_by_bookname(bookname)
    # notion_notes = parser.notes_to_page_content(notes)

    api_actions = NotionApiActions(database_id=database_id)
    page_id = api_actions.get_pages_by_name(page_name)[0]['id']
    api_actions.append_content(page_id, notion_notes)
