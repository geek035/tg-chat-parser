from abc import ABC, abstractmethod
from custom_types.messages_engine.message_analyzer_core import MessageAnalyzerResultType

class MessageAnalyzerBuffered(ABC):
    @abstractmethod
    def concat_data(self, new_data: MessageAnalyzerResultType, buffered_data: MessageAnalyzerResultType):
        pass