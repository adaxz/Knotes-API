import os

TEST_MODE = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if TEST_MODE:
    FIEL_DIR = os.path.join(BASE_DIR, 'test', 'files')
