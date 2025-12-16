import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from redis.asyncio import Redis

from .config import load_config
from .handlers import router
from .llm import LLM
from .memory import RedisMemoryRepository


async def run() -> None:
    """Сборка и запуск пуллинга бота."""
    env = Env()
    env.read_env()
    config = load_config(env=env)

    logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO)

    redis = Redis.from_url(url=config.redis_url)
    memory_repository = RedisMemoryRepository(redis_client=redis, history_limit=15)
    llm = LLM(
        api_key=config.llm_api_key,
        model=config.llm_model,
        base_url=config.llm_base_url,
        memory_repository=memory_repository,
    )
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(
        storage=RedisStorage(redis=redis), llm=llm, memory_repository=memory_repository,
    )
    dp.include_router(router)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await redis.close()
