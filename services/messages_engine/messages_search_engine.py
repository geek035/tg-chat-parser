from custom_types.messages_engine.message_search_engine_core import MessagesSearchEngineCore
from custom_types.messages_engine.message_analyzer_buffer import MessageAnalyzerBuffered
from custom_types.repositories.messages_engine_repository_core import MessagesEngineRepositoryCore
from telethon import TelegramClient
from typing import TypedDict

class MessagesSearchEngineBuffer(TypedDict):
    min_id: int
    data: dict


class MessagesSearchEngine(MessagesSearchEngineCore):
    """
    Класс для обзора истории сообщений чата и поиска информации в сообщениях
    по заданному списку конфигураций из анализаторов сообщений
    """
    def __init__(self, repository: MessagesEngineRepositoryCore): 
        super().__init__()

        if (repository is None):
            raise ValueError("Не передан репозиторий")

        self.__repository = repository

    async def search_in_history(self, client: TelegramClient, chat: str) -> dict:
        local_data = await self.__check_repository(client, chat)

        collected_data: MessagesSearchEngineBuffer = local_data if len(local_data) else {
            "min_id": 0,
            "data": {}
        }

        min_id = collected_data["min_id"]

        async for message in client.iter_messages(chat, min_id=min_id):
            for analyzer in self.configuration:
                await analyzer.analysis_message(message)
        
        for analyzer in self.configuration:
            result = analyzer.get_result()
            if (isinstance(analyzer, MessageAnalyzerBuffered)):
                collected_data["data"][result["key"]] = analyzer.concat_data(result, collected_data["data"].get(result["key"], {}))
            else:
                collected_data["data"][result["key"]] = result["value"]
        
        min_id = await self.__get_last_message_id(client, chat)
        collected_data["min_id"] = min_id

        await self.__repository.update_entity(client, chat, collected_data)

        return collected_data
    
    async def __check_repository(self, client: TelegramClient, chat: str) -> MessagesSearchEngineBuffer:
        data = await self.__repository.read_by_id(client)
        return data.get(chat, {})

    async def __get_last_message_id(self, client: TelegramClient, chat: str):
        messages = await client.get_messages(chat, limit=1)
        if messages:
            last_message = messages[0]
            return last_message.id
        else:
            return None


    