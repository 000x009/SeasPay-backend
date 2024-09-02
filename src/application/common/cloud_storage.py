from typing import Protocol
from abc import abstractmethod


class CloudStorage(Protocol):
    @abstractmethod
    def upload_file(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def delete_file(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def download_file(self) -> str:
        raise NotImplementedError
