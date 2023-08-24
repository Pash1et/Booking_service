from fastapi import HTTPException


class CustomException(HTTPException):
    status_code = None
    detail = None

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)
