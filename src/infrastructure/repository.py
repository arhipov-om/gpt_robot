"""Модуль для работы с хранилищем Redis."""

from langchain_community.chat_message_histories import RedisChatMessageHistory


class RedisMemoryRepository:
    """Репозиторий для работы с памятью в Redis."""

    def __init__(self, redis_url: str) -> None:
        """Инициализирует репозиторий.

        :param redis_url: ЮРЛ для подключения Redis.
        """
        self.redis_url = redis_url

    async def get_chat_history(self, chat_id: int) -> RedisChatMessageHistory:
        """Возвращает историю чата из Redis.

        :param chat_id: ID чата.
        :return: Объект истории чата.
        """
        return RedisChatMessageHistory(session_id=str(chat_id), url=self.redis_url)

    async def add_user_message(self, chat_id: int, message: str) -> None:
        """Добавляет сообщение пользователя в историю.

        :param chat_id: ID чата.
        :param message: Сообщение пользователя.
        """
        history = await self.get_chat_history(chat_id)
        history.add_user_message(message)

    async def add_ai_message(self, chat_id: int, message: str) -> None:
        """Добавляет сообщение от AI в историю.

        :param chat_id: ID чата.
        :param message: Сообщение от AI.
        """
        history = await self.get_chat_history(chat_id)
        history.add_ai_message(message)

    async def clear_chat_history(self, chat_id: int) -> None:
        """Очищает историю чата.

        :param chat_id: ID чата.
        """
        history = await self.get_chat_history(chat_id)
        history.clear()
