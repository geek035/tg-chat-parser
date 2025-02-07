from custom_types.messages_engine.message_analyzer_core import MessageAnalyzerCore
from custom_types.messages_engine.message_analyzer_core import MessageAnalyzerResultType
from custom_types.messages_engine.message_analyzer_buffer import MessageAnalyzerBuffered
from custom_types.messages_engine.message_anaylzer_params import MessageAnalyzerParams

from telethon.types import Message, ReactionEmoji, ReactionCustomEmoji
from typing import TypedDict, List

from copy import deepcopy

class ReactionsCounterAnalyzerParamsType(TypedDict):
    emoji: List[str]
    custom_emoji: List[int]

class ReactionsCounterAnalyzerResultType(MessageAnalyzerResultType):
    pass

class ReactionsCounterMessageAnalyzer(
    MessageAnalyzerCore, 
    MessageAnalyzerParams, 
    MessageAnalyzerBuffered):

    """
    Анализатор кол-ва реакций на сообщении
    """

    def __init__(self, params):
        MessageAnalyzerParams.__init__(self, params)
        super().__init__(params)

        self._result = {
            "key": "reactionsAnalysis",
            "value": {}
        }

    async def analysis_message(self, message: Message):
        reactions = message.reactions

        if reactions is None:
            return

        for reaction in reactions.results:
                if isinstance(reaction.reaction, ReactionEmoji):
                    emoji = reaction.reaction.emoticon
            
                    if (emoji in self._params["emoji"]):
                        emoji_count = self._result["value"].get(emoji, 0)
                        self._result["value"][emoji] = emoji_count + 1

                elif isinstance(reaction.reaction, ReactionCustomEmoji):
                    custom_emoji = reaction.reaction.document_id

                    if (custom_emoji in self._params["custom_emoji"]):
                        custom_emoji_count = self._result["value"].get(custom_emoji, 0)
                        self._result["value"][custom_emoji] = custom_emoji_count + 1
    
    def concat_data(self, new_data: ReactionsCounterAnalyzerResultType, 
        buffered_data: dict) -> ReactionsCounterAnalyzerResultType:

        if not len(buffered_data):
            return new_data["value"]
    
        concat_data = deepcopy(buffered_data)
        for key, value in new_data["value"].items():
            concat_data[key] = buffered_data.get(key, 0) + value

        return concat_data

    def get_result(self) -> ReactionsCounterAnalyzerResultType:
        return self._result

    def _validate_params(self, params: ReactionsCounterAnalyzerParamsType):
        required_keys = {"emoji", "custom_emoji"}

        if not isinstance(params, dict):
            raise TypeError("Параметры должны быть словарем.")
        
        if not required_keys.issubset(params.keys()):
            raise ValueError(f"Параметры должны содержать ключи: {required_keys}")

        return