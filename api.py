from fastapi import FastAPI

app = FastAPI()

'''
- /kindle/booknames
    - return all booknames in 'My Cippings.txt'
- /kobo/booknames
    - return all booknames in 'KoboReader.sqlite'
- /kindle/notes/?bookname={bookname}
    - return all notes for the given bookname in kindle notes
- /kobo/notes/?bookname={bookname}
    - return all notes for the given bookname in kobo notes

Further
    - kobo word list
    - kobo reading status
'''


@app.get("/")
async def root():
    return {"message": "Hello World"}
