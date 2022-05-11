import os

TEST_MODE = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if TEST_MODE:
    pass
    # FIEL_DIR = os.path.join(BASE_DIR, 'test', 'files')

FIEL_DIR = os.path.join(BASE_DIR, 'files')
KOBO_DB_DIR = os.path.join(BASE_DIR, 'files', 'KoboReader.sqlite')
BASH_DIR = os.path.join(BASE_DIR, 'senders', 'append.sh')
