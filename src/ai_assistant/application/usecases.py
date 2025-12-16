"""Модуль с use cases бизнес логики."""

import logging

from ai_assistant.application.services import MemoryService
from ai_assistant.infrastructure.llm.llm import LLM

logger = logging.getLogger("UseCase")


class GetLLMAnswerUseCase:
    """Use case для получения ответа от LLM с учётом истории диалога."""

    def __init__(
        self,
        llm: LLM,
        memory_service: MemoryService,
        prompt: str | None = None,
    ) -> None:
        self.llm = llm
        self.memory_service = memory_service
        self.prompt = prompt or (
            "The following is a friendly conversation between a human and an AI. "
            "The AI is talkative and "
            "provides lots of specific details from its context. "
            "If the AI does not know the answer to a "
            "question, it truthfully says it does not know."
        )

    async def execute(
        self,
        user_message: str,
        chat_id: int,
    ) -> str:
        """Делает запрос к LLM сервису и сохраняет сообщения в историю."""
        messages = [{"system": self.prompt}]
        await self.memory_service.add_user_message(
            user_message=user_message,
            chat_id=chat_id,
        )
        history = await self.memory_service.get_chat_history(chat_id=chat_id)
        messages.extend(history)
        ai_message = await self.llm.completions(messages=messages)
        await self.memory_service.add_ai_message(ai_message=ai_message, chat_id=chat_id)
        logger.debug(ai_message)
        return ai_message
