from enum import Enum


class UploadFileTypes(Enum):
    """
    Enum describing how data is provided
    """
    COMPRESSED = 'application/x-zip-compressed'
