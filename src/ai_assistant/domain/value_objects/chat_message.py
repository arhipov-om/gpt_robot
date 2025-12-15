"""Value object для сообщения чата с LLM."""

from typing import Literal, TypedDict


class ChatMessage(TypedDict):
    """Типизированный словарь сообщения чата."""

    role: Literal["user", "assistant"]
    content: str
