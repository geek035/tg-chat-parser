from custom_types.messages_engine.message_search_engine_core import MessagesSearchEngineCore
from custom_types.messages_engine.message_analyzer_core import MessageAnalyzerCore
from custom_types.repositories.messages_engine_repository_core import MessagesEngineRepositoryCore

class MessagesSearchEngineConfigurator():
    def __init__(self, message_engine: MessagesSearchEngineCore, 
                 repository: MessagesEngineRepositoryCore = None):
        if not isinstance(message_engine, type):
            raise TypeError("Переданный аргумент message_engine не является типом")
        
        if (not repository is None and not isinstance(repository, MessagesEngineRepositoryCore)):
            raise TypeError("Переданный аргумент repository не является экземпляром класса")

        self.__message_engine = message_engine(repository)

    def reset(self):
        self.__message_engine.configuration = []
    
    def add_analyzer(self, analyzer: MessageAnalyzerCore, param: dict):
        if not isinstance(analyzer, type):
            raise TypeError("Переданный аргумент analyzer не является типом")
        
        try:
            analyzer_inst = analyzer(param)

            self.__message_engine.configuration.append(analyzer_inst)

        except Exception as e:
            print(f"Ошибка: {e}")
            return
        
    def get_search_engine(self):
        return self.__message_engine