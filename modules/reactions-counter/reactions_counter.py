from telethon import TelegramClient
from reactions_dict import ReactionsDict

class ReactionsCounter:
    @staticmethod
    async def count_reactions(client: TelegramClient, source: str, reactions: ReactionsDict):
        source = client.get_entity(source)
        
