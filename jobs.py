import config
import os


class KindleNotesParser:
    def __init__(self, text_or_filename: str) -> None:
        self.isFile = False
        if text_or_filename.split('.')[-1] == 'txt':
            self.isFile = True
            self.filename = text_or_filename
        else:
            self.text = text_or_filename

    def _read_txt(self):
        fp = os.path.join(config.FIEL_DIR, self.filename)
        with open(fp, 'r') as txt_file:
            self.text = txt_file.read()


if __name__ == "__main__":
    filename = 'My Clippings.txt'
    parser = KindleNotesParser(filename)
    parser._read_txt()
