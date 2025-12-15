"""Точка входа."""
import asyncio

from ai_assistant.presentation.telegram.main import run

if __name__ == "__main__":
    asyncio.run(run())
