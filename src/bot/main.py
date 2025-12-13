"""Точка входа бота."""

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from langchain_openai import ChatOpenAI
from redis.asyncio import ConnectionPool, Redis

from bot.handlers import router
from infrastructure.repository import RedisMemoryRepository


async def run() -> None:
    """Сборка и запуск пуллинга бота."""
    env = Env()
    env.read_env()
    redis_url = env.str("REDIS_URL")

    logging.basicConfig(level=logging.DEBUG if env.bool("DEBUG") else logging.INFO)

    pool = ConnectionPool.from_url(url=redis_url)
    redis = Redis(connection_pool=pool)
    llm = ChatOpenAI(
        api_key=env.str("LLM_API_KEY"),
        base_url=env.str("LLM_BASE_URL", None),
        model=env.str("LLM_MODEL"),
    )
    memory_repository = RedisMemoryRepository(redis_url)
    bot = Bot(
        token=env.str("BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(
        storage=RedisStorage(redis=redis),
        llm=llm,
        memory_repository=memory_repository,
    )
    dp.include_router(router)
    await dp.start_polling(bot)
