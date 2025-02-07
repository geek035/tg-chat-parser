from custom_types.repositories.messages_engine_repository_core import MessagesEngineRepositoryCore
from telethon import TelegramClient
import aiofiles
import aiofiles.os
import logging
import json
import os

class JSONFileRepository(MessagesEngineRepositoryCore):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__repository = os.path.join(os.path.dirname(__file__), "local_storage.json")

    async def read_all(self) -> list[str]:
        try:
            if not os.path.exists(self.__repository):
                return {}

            async with aiofiles.open(self.__repository, mode='r', encoding='utf-8') as file:
                data = await file.read()
                return json.loads(data)

        except OSError as e:
            logging.error(f"Ошибка при чтении файла: {e}")
            return []

    
    async def read_by_id(self, client: TelegramClient) -> dict:
            try:
                user = await client.get_me()
                entities = await self.read_all()
                return entities.get(user.id, {})

            except OSError as e:
                logging.error(f"Ошибка при чтении файла: {e}")
                return {}
            
    async def update_entity(self, client: TelegramClient, chat: str, data: dict) -> None:
        user = await client.get_me()
        entities = await self.read_all()

        user_id_str = str(user.id)

        # Инициализируем данные для пользователя, если их нет
        if user_id_str not in entities:
            entities[user_id_str] = {}

        # Обновляем данные конкретного чата
        entities[user_id_str][chat] = data
        
        try:
            async with aiofiles.open(self.__repository, mode='w', encoding='utf-8') as file:
                await file.write(json.dumps(entities))
        except OSError as e:
            logging.error(f"Ошибка при записи файла: {e}")
            return
        
