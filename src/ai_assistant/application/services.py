"""Сервисы для работы с бизнес логикой."""
from ai_assistant.domain.interfaces.memory_repository import IMemoryRepository
from ai_assistant.domain.value_objects.chat_message import ChatMessage


# Точка масштабирования
class MemoryService:
    def __init__(self, memory_repository: IMemoryRepository) -> None:
        self.repo = memory_repository

    async def add_user_message(self, chat_id: int, user_message: str) -> None:
        return await self.repo.add_user_message(chat_id=chat_id, message=user_message)

    async def add_ai_message(self, chat_id: int, ai_message: str) -> None:
        return await self.repo.add_ai_message(chat_id=chat_id, message=ai_message)

    async def get_chat_history(
        self, chat_id: int,
    ) -> list[ChatMessage] | list[dict[str, str]]:
        return await self.repo.get_chat_history(chat_id=chat_id)

    async def clear(self, chat_id: int) -> None:
        return await self.repo.clear_chat_history(chat_id=chat_id)
