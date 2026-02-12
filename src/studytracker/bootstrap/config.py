import os
from dataclasses import dataclass
from pathlib import Path

import toml_rs
from adaptix import Retort

from studytracker.infrastructure.database.config import DatabaseConfig
from studytracker.presentation.config import ApiConfig

retort = Retort()


@dataclass(slots=True, kw_only=True)
class Config:
    database_config: DatabaseConfig
    api_config: ApiConfig


def get_config_path() -> Path:
    if (env_var := os.getenv("APP_CONFIG_PATH")) is None:
        raise RuntimeError("Missing env `APP_CONFIG_PATH`")
    return Path(env_var)


def load_config(path: Path) -> Config:
    file = path.read_text("utf-8")
    return retort.load(toml_rs.loads(file, toml_version="1.1.0"), Config)
