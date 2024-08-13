from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class QbitWeb(BaseSettings):
    url: AnyUrl
    username: str
    password: str
    unsafe_cookies: bool = False


class Settings(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
    )

    qbitweb: QbitWeb


@lru_cache(maxsize=1)
def get_settings():
    return Settings()
