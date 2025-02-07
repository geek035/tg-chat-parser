from custom_types.messages_engine.message_analyzer_core import MessageAnalyzerCore
from custom_types.messages_engine.message_analyzer_core import MessageAnalyzerResultType
from custom_types.messages_engine.message_anaylzer_params import MessageAnalyzerParams
from custom_types.messages_engine.message_analyzer_buffer import MessageAnalyzerBuffered
from telethon.tl.functions.messages import GetMessageReactionsListRequest

from telethon.types import Message, ReactionEmoji
from telethon import TelegramClient
from typing import TypedDict

from copy import deepcopy
import re

class HeartUsesAnalyzerParamsType(TypedDict):
    client: TelegramClient

class HeartUsesAnalyzerResultType(MessageAnalyzerResultType):
    pass

class HeartUsesAnalyzer(
    MessageAnalyzerCore,
    MessageAnalyzerParams,
    MessageAnalyzerBuffered):

    def __init__(self, params: HeartUsesAnalyzerParamsType):
        MessageAnalyzerParams.__init__(self, params)
        super().__init__()

        self._result = {
            "key": "heartAnalysis",
            "value": {}
        }

        self.__heart_emojis = [
            '❤️', '💔', '💕', '💖', '💗', '💓', '💞', '💘',
            '💝', '💟', '❣️', '♥️'
        ]

    async def analysis_message(self, message: Message):
        heart_count = 0

        if (message.text is not None):
            heart_count += self.__count_heart_emoji(message.text)

        if (message.reactions):
            try:
                users_who_reacted = await self._params["client"](GetMessageReactionsListRequest(
                    peer=message.peer_id,
                    id=message.id,
                    reaction=ReactionEmoji(emoticon='❤️'),
                    limit=2
                ))

                for user in users_who_reacted.users:
                    self._result["value"][user.id] = self._result["value"].get(user.id, 0) + 1

            except Exception as e:
                print(f"Ошибка при получении реакций: {e}")

        sender = await message.get_sender()
        self._result["value"][sender.id] = self._result["value"].get(sender.id, 0) + heart_count
    
    def concat_data(self, new_data, buffered_data):
        if not len(buffered_data):
            return new_data["value"]

        concat_data = deepcopy(buffered_data)
        for key, value in new_data["value"].items():
            concat_data[key] = buffered_data.get(key, 0) + value

        return concat_data
    
    def get_result(self):
        return self._result
    
    def _validate_params(self, params: HeartUsesAnalyzerParamsType):
        required_keys = {"client"}

        if not isinstance(params, dict):
            raise TypeError("Параметры должны быть словарем.")
        
        if not required_keys.issubset(params.keys()):
            raise ValueError(f"Параметры должны содержать ключи: {required_keys}")
        
        if not isinstance(params["client"], TelegramClient):
            raise TypeError("Клиент должен быть объектом TelegramClient.")

    def __count_heart_emoji(self, message_text):
        heart_pattern = re.compile('|'.join(map(re.escape, self.__heart_emojis)))
        return len(heart_pattern.findall(message_text))