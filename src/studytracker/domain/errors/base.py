from dataclasses import dataclass
from enum import StrEnum
from typing import dataclass_transform


@dataclass_transform(kw_only_default=True)
def app_error[ClsT](cls: type[ClsT]) -> type[ClsT]:
    return dataclass(slots=True, kw_only=True, frozen=True, eq=False)(cls)


class ErrorCode(StrEnum):
    NOT_FOUND = "NOT_FOUND"
    INVALID_PERIOD_RANGE = "INVALID_PERIOD_RANGE"


@app_error
class AppError(Exception):
    code: ErrorCode
    status_code: int

    @property
    def message() -> str:
        raise NotImplementedError
