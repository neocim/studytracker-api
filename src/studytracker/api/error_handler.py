import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from studytracker.application.errors.goal import GoalNotFoundError, ParentGoalNotFoundError
from studytracker.domain.errors.base import AppError
from studytracker.domain.errors.goal import (
    InvalidPeriodRangeError,
    InvalidStatusForActiveGoalError,
    InvalidStatusForCompletedGoalError,
    InvalidStatusForNotStartedGoalError,
    InvalidSubgoalPeriodRangeError,
)
from studytracker.infrastructure.http.errors import ErrorResponse, InternalServerError

logger = logging.getLogger(__name__)

error_to_http_status: dict[type[AppError], int] = {
    ParentGoalNotFoundError: 404,
    GoalNotFoundError: 404,
    InvalidPeriodRangeError: 422,
    InvalidSubgoalPeriodRangeError: 422,
    InvalidStatusForNotStartedGoalError: 422,
    InvalidStatusForActiveGoalError: 422,
    InvalidStatusForCompletedGoalError: 422,
}


def get_app_error_response(app_error: AppError) -> JSONResponse:
    try:
        http_status = error_to_http_status[type(app_error)]
    except KeyError:
        class_type = (
            app_error.__class__.__qualname__
            if not isinstance(app_error, InternalServerError)
            else app_error.exception.__class__.__qualname__
        )
        logger.critical("AppError is missing status code mapping: %s", class_type)
        http_status = 500

    error_response = ErrorResponse(
        code=app_error.code,
        message=app_error.message,
    ).model_dump_json()
    logger.info("Handled error: %s", app_error)

    return JSONResponse(status_code=http_status, content=error_response)


async def app_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    app_error = exc if isinstance(exc, AppError) else None

    if app_error is None:
        logger.critical("Unexpected internal server error: %s", exc)
        app_error = InternalServerError(exception=exc)

    return get_app_error_response(app_error)
