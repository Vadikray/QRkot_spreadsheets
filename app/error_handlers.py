from fastapi import HTTPException


class NameDuplicateException(HTTPException):
    pass


class MissingProjectException(HTTPException):
    pass


class EditProjectException(HTTPException):
    pass