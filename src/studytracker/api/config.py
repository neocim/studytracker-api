from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class ApiConfig:
    host: str
    port: int
