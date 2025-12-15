"""Модуль для работы с LLM."""

from httpx import AsyncClient

from domain.interfaces.memory_repository import IMemoryRepository
from domain.value_objects.chat_message import ChatMessage


def prepare_request(history: list[ChatMessage]) -> dict:
    return history


class LLM:
    def __init__(
        self,
        api_key: str,
        model: str,
        memory_repository: IMemoryRepository,
        base_url: str | None = None,
    ) -> None:
        self.__base_url = base_url or "https://api.openai.com/v1/"
        self.model = model
        self.memory_repository = memory_repository
        self.http_client = self.__get_http_client(api_key=api_key)

    def __get_http_client(self, api_key: str) -> AsyncClient:
        return AsyncClient(
            base_url=self.__base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    async def get_ai_answer(self, user_message: str, chat_id: int) -> str:
        """Генерирует ответ от LLM."""
        await self.memory_repository.add_user_message(
            chat_id=chat_id, message=user_message
        )
        history = await self.memory_repository.get_chat_history(chat_id=chat_id)
        request = prepare_request(history=history)
        payload = {"model": self.model, "input": request}
        response = await self.http_client.post(url="/responses", json=payload)
        ai_answer = (
            response.json().get("output", [{}])[0].get("content", [{}])[0].get("text")
        )
        await self.memory_repository.add_ai_message(chat_id=chat_id, message=ai_answer)
        return ai_answer

