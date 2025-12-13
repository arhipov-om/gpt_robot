from aiogram import F, Router
from aiogram.types import Message
from langchain_core.language_models import BaseChatModel

from infrastructure.llm import get_llm_text
from infrastructure.repository import RedisMemoryRepository

router = Router()


@router.message(F.text)
async def process_text_message(
    message: Message,
    llm: BaseChatModel,
    memory_repository: RedisMemoryRepository,
) -> None:
    """Обрабатывает входящие текстовые сообщения."""
    llm_answer = await get_llm_text(
        llm=llm,
        memory_repository=memory_repository,
        input_query=message.text,
        chat_id=message.chat.id,
    )
    await message.answer(text=llm_answer)
