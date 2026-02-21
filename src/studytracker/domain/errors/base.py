from dataclasses import dataclass
from typing import ClassVar, dataclass_transform


@dataclass_transform(kw_only_default=True)
def app_error[ClsT](cls: type[ClsT]) -> type[ClsT]:
    return dataclass(slots=True, kw_only=True, frozen=True, eq=False)(cls)


@app_error
class AppError(Exception):
    code: ClassVar[str]

    @property
    def message(self) -> str:
        raise NotImplementedError
