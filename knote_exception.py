from config import VALID_FILE_EXTENSION
from parsers.models import DeviceType


class NotProperDeviceTypeException(Exception):
    def __init__(self, msg) -> None:
        self.message = msg


class NotProperFileFormatException(Exception):
    def __init__(self, msg) -> None:
        self.message = msg
