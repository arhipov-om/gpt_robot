"""Модуль с конфигурацией приложения."""
from dataclasses import dataclass

from environs import Env


@dataclass(frozen=True)
class Config:
    """Датакласс содержащий конфигурации приложения."""

    debug: bool
    bot_token: str
    redis_url: str
    llm_api_key: str
    llm_base_url: str | None
    llm_model: str


def load_config(env: Env) -> Config:
    """Создает и возвращает Config из переменных окружения."""
    return Config(
        debug=env.bool("DEBUG", False),
        bot_token=env.str("BOT_TOKEN"),
        redis_url=env.str("REDIS_URL"),
        llm_api_key=env.str("LLM_API_KEY"),
        llm_base_url=env.str("LLM_BASE_URL", None),
        llm_model=env.str("LLM_MODEL"),
    )
