import logging

from httpx import AsyncClient

from ai_assistant.memory import RedisMemoryRepository

logger = logging.getLogger("LLM")


class LLM:
    """Gateway для LLM."""

    def __init__(
        self,
        api_key: str,
        model: str,
        memory_repository: RedisMemoryRepository,
        base_url: str | None = None,
    ) -> None:
        self.__base_url = base_url or "https://api.openai.com/v1/"
        self.model = model
        self.http_client = self.__get_http_client(api_key=api_key)
        self.memory_repository = memory_repository

    def __get_http_client(self, api_key: str) -> AsyncClient:
        return AsyncClient(
            base_url=self.__base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    async def completions(
        self,
        user_message: str,
        chat_id: int,
        model: str | None = None,
    ) -> str:
        await self.memory_repository.add_user_message(
            message=user_message, chat_id=chat_id,
        )
        messages = await self.memory_repository.get_chat_history(chat_id=chat_id)
        payload = {"model": model or self.model, "messages": messages}
        response = await self.http_client.post(url="/chat/completions", json=payload)
        logger.debug("response: %s", response.json())
        ai_message = (
            response.json().get("choices", [{}])[0].get("message", {}).get("content")
        )
        await self.memory_repository.add_ai_message(message=ai_message, chat_id=chat_id)
        return ai_message
