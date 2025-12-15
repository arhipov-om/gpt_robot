"""Модуль с фабрикой для создания LLM."""

from ai_assistant.config import Config
from ai_assistant.domain.interfaces.memory_repository import IMemoryRepository

from .llm import LLM


def create_llm(config: Config, memory_repository: IMemoryRepository) -> LLM:
    """Создает и возвращает LLM."""
    return LLM(
        api_key=config.llm_api_key,
        base_url=config.llm_base_url,
        model=config.llm_model,
        memory_repository=memory_repository,
    )
