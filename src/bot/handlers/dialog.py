from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def process_text_message(message: Message) -> None:
    """Обрабатывает входящие текстовые сообщения."""
    await message.answer(text=message.text)
