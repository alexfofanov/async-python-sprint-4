from sys import modules

from pydantic import IPvAnyAddress
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    app_title: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_host: IPvAnyAddress | str
    db_port: int
    postgres_test_db: str
    db_test_port: int
    project_host: IPvAnyAddress
    project_port: int
    block_subnets: list[str]
    token_size: int

    class Config:
        env_file = '.env' if 'pytest' in modules else '.env'

    @property
    def dsn(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres_user}:'
            f'{self.postgres_password}@{self.db_host}:'
            f'{self.db_port}/{self.postgres_db}'
        )

    @property
    def dsn_test(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres_user}:'
            f'{self.postgres_password}@{self.db_host}:'
            f'{self.db_test_port}/{self.postgres_test_db}'
        )


app_settings = AppSettings()
