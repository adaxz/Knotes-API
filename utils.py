import config
import uuid
from parsers.models import DeviceType
import os
from knote_exception import NotProperDeviceTypeException, NotProperFileFormatException


def validate_file(type: str, origin_filename: str) -> bool:
    _, file_ext = os.path.splitext(origin_filename)
    if file_ext not in config.VALID_FILE_EXTENSION:
        raise NotProperFileFormatException(
            f"File format {file_ext} is not allowed. Only {config.VALID_FILE_EXTENSION} is allowed")
    else:
        if file_ext == '.txt' and type == DeviceType.KOBO.value:
            raise NotProperFileFormatException(
                f"File format {file_ext} is not allowed with device type {type}. Only .sqlite is allowed with device type kobo")
        elif file_ext == '.sqlite' and type == DeviceType.KINDLE.value:
            raise NotProperFileFormatException(
                f"File format {file_ext} is not allowed with device type {type}. Only .txt is allowed with device type kobo")


def form_file_path(type: str, origin_filename: str) -> str:
    if type not in DeviceType.to_list():
        raise NotProperDeviceTypeException(
            f"Device type {type} is not recoginized. Device type must be in {DeviceType.to_list()}")

    validate_file(type, origin_filename)

    _, file_ext = os.path.splitext(origin_filename)
    filename = str(uuid.uuid4().hex) + file_ext
    file_path = os.path.join(config.FILE_DIR, type, filename)
    return file_path
