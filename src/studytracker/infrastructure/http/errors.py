from typing import override

from pydantic import BaseModel

from studytracker.domain.errors.base import AppError, app_error


class ErrorResponse(BaseModel):
    code: str
    message: str


@app_error
class InternalServerError(AppError):
    code = "INTERNAL_SERVER_ERROR"
    exception: Exception

    @override
    @property
    def message(self) -> str:
        return "Internal server error"
