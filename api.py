from fastapi import FastAPI, HTTPException
from parsers.kindle_parser import KindleNotesParser
from parsers.kobo_parser import KoboNotesParser
from parsers.models import DeviceType

app = FastAPI()

'''
- /booknames?type={}&filename={}
    - return all booknames based on the query parameters
- /notes?type={}&bookname={}
    - return notes for the given type and bookname in the query parameters

Further
    - kobo word list
    - kobo reading status
'''


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/types")
async def get_type() -> list[str]:
    return DeviceType.to_list()


@app.get("/booknames/{filename}")
async def get_booknames(type: str, filename: str):
    if any([type is None, filename is None]):
        raise HTTPException(
            status_code=400, detail=f'One or more query parameters are missing')

    if type not in get_type():
        raise HTTPException(
            status_code=400, detail=f'Value of "type" shoud be either "kobo" or "kindle"')

    note_parser = KindleNotesParser(
        filename) if type == DeviceType.KINDLE else KoboNotesParser(filename)
    books = note_parser.get_all_books()

    return {'booknames': books}


@app.get("/notes/{filename}")
async def get_notes(type: str, bookname: str, filename: str):
    if any([type is None, bookname is None]):
        raise HTTPException(
            status_code=400, detail=f'One or more query parameters are missing')

    if type not in DeviceType.to_list():
        raise HTTPException(
            status_code=400, detail=f'Value of "type" shoud be either "kobo" or "kindle"')

    note_parser = KindleNotesParser(
        filename) if type == DeviceType.KINDLE else KoboNotesParser(filename)

    return {"notes": note_parser.get_notes_by_bookname(bookname)}
