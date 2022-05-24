import os

TEST_MODE = True

VALID_FILE_EXTENSION = ['.txt', '.sqlite']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if TEST_MODE:
    pass
    # FIEL_DIR = os.path.join(BASE_DIR, 'test', 'files')

FILE_DIR = os.path.join(BASE_DIR, 'files')
KOBO_FILE_DIR = os.path.join(FILE_DIR, 'kobo')
KINDLE_FILE_DIR = os.path.join(FILE_DIR, 'kindle')
KOBO_DB_DIR = os.path.join(BASE_DIR, 'files', 'KoboReader.sqlite')
BASH_DIR = os.path.join(BASE_DIR, 'senders', 'append.sh')

API_ORIGINS = ['http://localhost:4200']
