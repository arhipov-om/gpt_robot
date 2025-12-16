"""Обработчики для команд."""

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from ai_assistant.application.services import MemoryService

router = Router()

btn_text = "Новый запрос"


@router.message(CommandStart())
@router.message(F.text == btn_text)
async def process_start(
    message: Message,
    memory_service: MemoryService,
) -> None:
    """Обработчик для команды /start и реплай кнопки. Очищает историю при вызове."""
    await memory_service.clear(chat_id=message.chat.id)
    await message.answer("Начат новый диалог.\n\nПриветствую!")
    if message.text == btn_text:
        await message.delete()


@router.message(Command("help"))
async def process_help(message: Message) -> None:
    """Обработчик для команды /help."""
    await message.answer(
        text="Я ИИ ассистент который <b>запоминает</b> историю общения.\n"
        f"Для сброса беседы нажмите /start или кнопку <b>{btn_text}</b>",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=btn_text),
                ],
            ],
            resize_keyboard=True,
        ),
    )
