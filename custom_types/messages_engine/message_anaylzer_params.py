from abc import ABC, abstractmethod

class MessageAnalyzerParams(ABC):
    def __init__(self, params: dict) -> None:
        self._validate_params(params)
        self._params = params

    @abstractmethod
    def _validate_params(self, params: dict) -> None:
        pass
          