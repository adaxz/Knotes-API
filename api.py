from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from parsers.kindle_parser import KindleNotesParser
from parsers.kobo_parser import KoboNotesParser
from parsers.models import DeviceType
from knote_exception import NotProperDeviceTypeException, NotProperFileFormatException
from utils import form_file_path
from config import API_ORIGINS
import os

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/types")
async def get_type() -> list[str]:
    return DeviceType.to_list()


@app.get("/booknames/{type}/{filename}")
async def get_booknames(type: str, filename: str):
    if any([type is None, filename is None]):
        raise HTTPException(
            status_code=400, detail=f'One or more query parameters are missing')

    if type not in DeviceType.to_list():
        raise HTTPException(
            status_code=400, detail=f'Value of "type" shoud be either "kobo" or "kindle"')

    note_parser = KindleNotesParser(
        filename) if type == DeviceType.KINDLE.value else KoboNotesParser(filename)
    books = note_parser.get_all_books()

    return {'booknames': books}


@app.get("/notes/{type}/{filename}/{bookname}")
async def get_notes(type: str, bookname: str, filename: str):
    if any([type is None, bookname is None]):
        raise HTTPException(
            status_code=400, detail=f'One or more query parameters are missing')

    if type not in DeviceType.to_list():
        raise HTTPException(
            status_code=400, detail=f'Value of "type" shoud be either "kobo" or "kindle"')

    note_parser = KindleNotesParser(
        filename) if type == DeviceType.KINDLE.value else KoboNotesParser(filename)

    return {"notes": note_parser.get_notes_by_bookname(bookname)}


@app.post("/upload/{type}")
async def upload(type: str, file: UploadFile = File(...)):
    origin_filename = file.filename

    try:
        file_path = form_file_path(type, origin_filename)
        filename = os.path.basename(file_path)
    except (NotProperDeviceTypeException, NotProperFileFormatException) as e:
        raise HTTPException(
            status_code=400, detail=f'There was an error uploading the file {e.message}')

    try:
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        return {"filename": str(filename)}
    except Exception:
        raise HTTPException(
            status_code=500, detail=f'There was an error uploading the file: {e}')
