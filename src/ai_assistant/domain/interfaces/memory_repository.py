"""Модуль с интерфейсом репозитория истории сообщений."""

from abc import ABC, abstractmethod


class IMemoryRepository(ABC):
    """Интерфейс для работы с историей сообщений."""

    @abstractmethod
    async def get_chat_history(self, chat_id: int) -> list:
        """Возвращает историю чата из репозитория.

        :param chat_id: ID чата.
        :return: Объект истории чата.
        """

    @abstractmethod
    async def add_user_message(self, chat_id: int, message: str) -> None:
        """Добавляет сообщение пользователя в историю.

        :param chat_id: ID чата.
        :param message: Сообщение пользователя.
        """

    @abstractmethod
    async def add_ai_message(self, chat_id: int, message: str) -> None:
        """Добавляет сообщение от AI в историю.

        :param chat_id: ID чата.
        :param message: Сообщение от AI.
        """

    @abstractmethod
    async def clear_chat_history(self, chat_id: int) -> None:
        """Очищает историю чата.

        :param chat_id: ID чата.
        """
