"""Модуль для работы с LLM."""

import logging

from httpx import AsyncClient

from ai_assistant.domain.value_objects.chat_message import ChatMessage

logger = logging.getLogger("LLM")


class LLM:
    """Gateway для LLM."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str | None = None,
    ) -> None:
        self.__base_url = base_url or "https://api.openai.com/v1/"
        self.model = model
        self.http_client = self.__get_http_client(api_key=api_key)

    def __get_http_client(self, api_key: str) -> AsyncClient:
        return AsyncClient(
            base_url=self.__base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    async def completions(
        self, messages: list[dict] | list[ChatMessage], model: str | None = None,
    ) -> str:
        """Делает http запрос к LLM сервису.

        :param messages: Список с сообщениями в формате словать role/content.
        :param model: LLM модель для запроса, по умолчанию возьмется,
         та которая указа при создании экземпляра.
        :return str: Ответ от LLM модели.
        """
        payload = {"model": model or self.model, "messages": messages}
        response = await self.http_client.post(url="/chat/completions", json=payload)
        logger.debug("response: %s", response.json())
        return response.json().get("choices", [{}])[0].get("message", {}).get("content")
