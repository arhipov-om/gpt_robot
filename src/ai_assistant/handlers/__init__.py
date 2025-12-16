__all__ = ("router",)

from aiogram import Router

from .commands import router as cmd_router
from .dialog import router as dialog_router

router = Router()

router.include_router(cmd_router)
router.include_router(dialog_router)
