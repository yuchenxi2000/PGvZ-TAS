import abc

class JsonNamingPolicy(abc.ABC):
    @classmethod
    @property
    def CamelCase(cls) -> JsonNamingPolicy: ...
    @abc.abstractmethod
    def ConvertName(self, name: str) -> str: ...

