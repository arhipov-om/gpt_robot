"""Точка входа бота."""

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from redis.asyncio import ConnectionPool, Redis


async def run() -> None:
    """Сборка и запуск пуллинга бота."""
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.DEBUG if env.bool("DEBUG") else logging.INFO)

    pool = ConnectionPool.from_url(url=env.str("REDIS_URL"))
    redis = Redis(connection_pool=pool)
    bot = Bot(
        token=env.str("BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=RedisStorage(redis=redis))

    await dp.start_polling(bot)
