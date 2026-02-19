import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from studytracker.application.errors.goal import InvalidPeriodRangeError, ParentGoalNotFoundError
from studytracker.domain.errors.base import AppError
from studytracker.infrastructure.http.errors import ErrorResponse, InternalServerError

logger = logging.getLogger(__name__)

error_to_http_status: dict[type[AppError], int] = {
    InvalidPeriodRangeError: 422,
    ParentGoalNotFoundError: 404,
}


async def app_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    try:
        http_status = error_to_http_status[type(exc)]
    except KeyError:
        logger.critical(
            "AppError is missing status code mapping",
            error_type=exc.__class__.__qualname__
            if not isinstance(exc, InternalServerError)
            else exc.exception.__class__.__qualname__,
        )
        http_status = 500

    app_error = exc if isinstance(exc, AppError) else None

    if app_error is None:
        logger.critical("Unexpected internal server error")
        app_error = InternalServerError(exception=exc)

    error_response = ErrorResponse(
        code=app_error.code,
        message=app_error.message,
    ).model_dump_json()

    return JSONResponse(status_code=http_status, content=error_response)
