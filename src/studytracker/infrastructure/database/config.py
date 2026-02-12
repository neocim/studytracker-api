from dataclasses import dataclass

from sqlalchemy import URL


@dataclass(slots=True, kw_only=True)
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    db_name: str

    @property
    def connection_url(self) -> URL:
        host = self.host
        port = self.port
        user = self.user
        password = self.password
        db_name = self.db_name

        return URL.create(
            drivername="postgresql+asyncpg",
            host=host,
            port=port,
            username=user,
            password=password,
            database=db_name,
        )
