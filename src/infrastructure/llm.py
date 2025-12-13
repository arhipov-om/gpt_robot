"""Модуль для работы с LLM."""

from langchain_classic.chains.conversation.base import ConversationChain
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from src.infrastructure.repository import RedisMemoryRepository

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "The following is a friendly conversation between a human and an AI. The AI is talkative and "
            "provides lots of specific details from its context. If the AI does not know the answer to a "
            "question, it truthfully says it does not know.",
        ),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ],
)


async def get_llm_text(
    llm: BaseChatModel,
    memory_repository: RedisMemoryRepository,
    input_query: str,
    chat_id: int,
) -> str:
    """Получает текстовый ответ от LLM с учетом истории диалога пользователя.

    :param llm: Языковая модель.
    :param memory_repository: Репозиторий для получения истории сообщений.
    :param input_query: Входной запрос для LLM.
    :param chat_id: ID чата для управления историей.
    :return: Строка с ответом от LLM.
    """
    chat_history = await memory_repository.get_chat_history(chat_id)

    memory = ConversationBufferWindowMemory(
        memory_key="history",
        k=15,
        return_messages=True,
        chat_memory=chat_history,
    )

    conversation = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
    )

    response = await conversation.ainvoke(input=input_query)
    return response.get("response", "")
