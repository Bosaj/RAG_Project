from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FIle_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "FILE_UPLOAD_SUCCESS"
    FILE_UPLOAD_FAILED = "FILE_UPLOAD_FAILED"