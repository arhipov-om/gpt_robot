import json

from redis.asyncio import Redis


class RedisMemoryRepository:
    """Репозиторий для работы с памятью в Redis."""

    def __init__(self, redis_client: Redis, history_limit: int) -> None:
        """Инициализирует репозиторий.

        :param redis_client: Экземпляр асинхронного Redis-клиента.
        :param history_limit: Лимит скользящего окна сообщений.
        """
        self.redis = redis_client
        self.history_limit = history_limit

    @staticmethod
    def _key(chat_id: int) -> str:
        """Формирует ключ для хранения истории чата."""
        return f"message_store:{chat_id}"

    async def _add_message(self, chat_id: int, message: dict[str, str]) -> None:
        """Сохраняет сообщение в Redis."""
        key = self._key(chat_id=chat_id)
        await self.redis.lpush(key, json.dumps(message))
        await self.redis.ltrim(key, 0, self.history_limit - 1)

    async def add_user_message(self, chat_id: int, message: str) -> None:
        """Добавляет сообщение пользователя в историю."""
        await self._add_message(
            chat_id=chat_id,
            message={"role": "user", "content": message},
        )

    async def add_ai_message(self, chat_id: int, message: str) -> None:
        """Добавляет сообщение от AI в историю."""
        await self._add_message(
            chat_id=chat_id,
            message={"role": "assistant", "content": message},
        )

    async def get_chat_history(self, chat_id: int) -> list[dict[str, str]]:
        """Возвращает историю сообщений чата в порядке их добавления."""
        key = self._key(chat_id=chat_id)
        raw_messages = await self.redis.lrange(key, 0, -1)
        return [json.loads(item) for item in reversed(raw_messages)]

    async def clear_chat_history(self, chat_id: int) -> None:
        """Очищает историю чата."""
        key = self._key(chat_id=chat_id)
        await self.redis.delete(key)
