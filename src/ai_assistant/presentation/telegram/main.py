"""Точка входа бота."""

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from redis.asyncio import Redis

from ai_assistant.config import Config, load_config
from ai_assistant.infrastructure.cache.factory import (
    get_memory_repository,
    get_redis_client_with_connection_pool,
    get_redis_connection_pool,
)
from ai_assistant.infrastructure.llm.factory import create_llm
from ai_assistant.infrastructure.llm.llm import LLM

from .handlers import router


def create_bot(config: Config) -> Bot:
    """Создает и возвращает Bot."""
    return Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher(redis: Redis, llm: LLM) -> Dispatcher:
    """Создает и возвращает Dispatcher."""
    dp = Dispatcher(storage=RedisStorage(redis=redis), llm=llm)
    dp.include_router(router)
    return dp


async def run() -> None:
    """Сборка и запуск пуллинга бота."""
    env = Env()
    env.read_env()
    config = load_config(env=env)

    logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO)

    pool = get_redis_connection_pool(config=config)
    redis = get_redis_client_with_connection_pool(pool=pool)
    memory_repository = get_memory_repository(redis=redis, history_limit=15)
    llm = create_llm(config=config, memory_repository=memory_repository)
    bot = create_bot(config=config)
    dp = create_dispatcher(redis=redis, llm=llm)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await redis.close()
