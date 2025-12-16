"""Модуль для обработки текстовых сообщений."""

import logging

from aiogram import F, Router
from aiogram.types import Message

from ai_assistant.application.usecases import GetLLMAnswerUseCase

router = Router()

logger = logging.getLogger("dialogs_router")


@router.message(F.text)
async def process_text_message(
    message: Message,
    get_llm_answer_use_case: GetLLMAnswerUseCase,
) -> None:
    """Обрабатывает входящие текстовые сообщения, генерирует ответ через LLM."""
    wait_message = await message.answer("⌛")
    try:
        llm_answer = await get_llm_answer_use_case.execute(
            user_message=message.text,
            chat_id=message.chat.id,
        )
        await message.answer(text=llm_answer)
    except Exception as err:
        logger.exception("some error", exc_info=err)
        await message.answer(text="Что то я устал, давай попозже..")
    finally:
        await wait_message.delete()
