from telethon import TelegramClient

from services.repositories.json_file_repository import JSONFileRepository
from services.messages_engine.messages_search_configurator import MessagesSearchEngineConfigurator
from services.messages_engine.messages_search_engine import MessagesSearchEngine

from services.messages_engine.message_analyzers.reactions_analyzer import ReactionsCounterMessageAnalyzer
from services.messages_engine.message_analyzers.heart_analyzer import HeartUsesAnalyzer

import os

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
client = TelegramClient('me', api_id, api_hash)
    
async def main():
    repository = JSONFileRepository()
    configurator = MessagesSearchEngineConfigurator(MessagesSearchEngine, repository)
    configurator.add_analyzer(ReactionsCounterMessageAnalyzer, {
        "emoji": ['❤️'],
        "custom_emoji": []
    })

    configurator.add_analyzer(HeartUsesAnalyzer, {
        "client": client
    })

    search_engine = configurator.get_search_engine()
    data = await search_engine.search_in_history(client, 'me')
    
with client:
    client.loop.run_until_complete(main())