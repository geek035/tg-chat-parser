from abc import ABC, abstractmethod
from custom_types.messages_engine.message_analyzer_core import MessageAnalyzerCore

from telethon import TelegramClient

class MessagesSearchEngineCore(ABC):
    """
    Класс-ядро всех поисковиков по сообщениям
    """

    def __init__(self):
        self.configuration: list[MessageAnalyzerCore] = []

    @abstractmethod
    async def search_in_history(client: TelegramClient, chat: str) -> dict:
        pass