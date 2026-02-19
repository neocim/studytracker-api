from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class APIConfig:
    host: str
    port: int
