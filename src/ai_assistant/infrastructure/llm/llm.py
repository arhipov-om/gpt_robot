"""Модуль для работы с LLM."""

import logging

from httpx import AsyncClient

from ai_assistant.domain.interfaces.memory_repository import IMemoryRepository

logger = logging.getLogger("LLM")


class LLM:
    """Gateway для LLM."""

    def __init__(  # noqa: D107
        self,
        api_key: str,
        model: str,
        memory_repository: IMemoryRepository,
        base_url: str | None = None,
        prompt: str | None = None,
    ) -> None:
        self.__base_url = base_url or "https://api.openai.com/v1/"
        self.model = model
        self.prompt = prompt or self.__default_prompt()
        self.memory_repository = memory_repository
        self.http_client = self.__get_http_client(api_key=api_key)

    def __get_http_client(self, api_key: str) -> AsyncClient:
        return AsyncClient(
            base_url=self.__base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    @staticmethod
    def __default_prompt() -> str:
        return (
            "The following is a friendly conversation between a human and an AI. "
            "The AI is talkative and "
            "provides lots of specific details from its context. "
            "If the AI does not know the answer to a "
            "question, it truthfully says it does not know."
        )

    async def _save_user_message_to_history(self, chat_id: int, message: str) -> None:
        await self.memory_repository.add_user_message(chat_id=chat_id, message=message)

    async def _prepare_messages_for_request(self, chat_id: int) -> list[dict]:
        messages = [{"system": self.prompt}]

        history = await self.memory_repository.get_chat_history(chat_id=chat_id)
        messages.extend(history)
        logger.debug(messages)
        return messages

    async def _get_ai_response(self, messages: list[dict]) -> str:
        payload = {"model": self.model, "messages": messages}
        response = await self.http_client.post(url="/chat/completions", json=payload)
        logger.debug("response: %s", response.json())
        return response.json().get("choices", [{}])[0].get("message", {}).get("content")

    async def _save_ai_message_to_history(self, chat_id: int, ai_message: str) -> None:
        await self.memory_repository.add_ai_message(chat_id=chat_id, message=ai_message)

    async def get_ai_answer(self, user_message: str, chat_id: int) -> str:
        """Генерирует ответ от LLM."""
        await self._save_user_message_to_history(chat_id=chat_id, message=user_message)

        full_request = await self._prepare_messages_for_request(chat_id=chat_id)
        ai_answer = await self._get_ai_response(messages=full_request)
        if ai_answer:
            await self._save_ai_message_to_history(
                chat_id=chat_id,
                ai_message=ai_answer,
            )

        return ai_answer
