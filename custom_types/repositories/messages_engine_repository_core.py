from abc import ABC, abstractmethod
from telethon import TelegramClient

class MessagesEngineRepositoryCore(ABC):

    @abstractmethod
    async def read_by_id(self, client: TelegramClient) -> dict:
        pass

    @abstractmethod
    async def update_entity(self, client: TelegramClient, chat: str, data: dict) -> None:
        pass