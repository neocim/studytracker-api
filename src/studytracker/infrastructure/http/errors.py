from studytracker.domain.errors.base import AppError, app_error


@app_error
class InternalServerError(AppError):
    code="INTERNAL_SERVER_ERROR"
    

    @property
    def message(self) -> str:
        return "Internal server error"
