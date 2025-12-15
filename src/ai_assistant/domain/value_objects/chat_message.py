"""Value object для сообщения чата с LLM."""
from typing import TypedDict, Literal


class ChatMessage(TypedDict):
    """Типизированный словарь сообщения чата."""

    type: Literal["User", "AI"]
    content: str
