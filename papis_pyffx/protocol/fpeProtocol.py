from typing import Protocol, Union

class FpeProtocol(Protocol):
    def encrypt(self, v : str) -> str:
        raise NotImplementedError

    def decrypt(self, v : str) -> str:
        raise NotImplementedError
    
    def encryptSet(self, di : Union[list, set]) -> dict:
        raise NotImplementedError
    
    def decryptSet(self, di : Union[list, set]) -> dict:
        raise NotImplementedError

    def maxQuerySize(self) -> int:
        raise NotImplementedError
    
    def alphabet(self) -> str:
        raise NotImplementedError