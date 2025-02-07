from abc import ABC, abstractmethod
from telethon.types import Message
from typing import List, TypedDict

class MessageAnalyzerResultType(TypedDict):
    key: str
    value: dict

class MessageAnalyzerCore(ABC):
    """
    Интерфейс анализаторов сообщения
    """
    
    def __init__(self, *args, **kwargs) -> None:
        self._result = {
            "key": "",
            "value": {}
        }
        

    @abstractmethod
    async def analysis_message(self, message: Message) -> None:
        pass

    @abstractmethod
    def get_result(self) -> MessageAnalyzerResultType:
        pass 