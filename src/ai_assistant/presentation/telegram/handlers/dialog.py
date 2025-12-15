"""Модуль для обработки текстовых сообщений."""

import logging

from aiogram import F, Router
from aiogram.types import Message
from langchain_core.language_models import BaseChatModel

from infrastructure.cache import RedisMemoryRepository
from infrastructure.llm import get_llm_text

router = Router()

logger = logging.getLogger("dialogs_router")


@router.message(F.text)
async def process_text_message(
    message: Message,
    llm: BaseChatModel,
    memory_repository: RedisMemoryRepository,
) -> None:
    """Обрабатывает входящие текстовые сообщения, генерирует ответ через LLM."""
    wait_message = await message.answer("⌛")
    try:
        llm_answer = await get_llm_text(
            llm=llm,
            memory_repository=memory_repository,
            input_query=message.text,
            chat_id=message.chat.id,
        )
        await wait_message.delete()
        await message.answer(text=llm_answer)
    except Exception as err:
        logger.exception("some error", exc_info=err)
        await wait_message.delete()
        await message.answer(text="Что то поломалось")
