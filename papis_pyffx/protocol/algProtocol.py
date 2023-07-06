from typing import Protocol, Union

class AlgProtocol(Protocol):
    def encrypt(self, v : Union[str, bytes]) -> Union[str, bytes]:
        raise NotImplementedError

    def decrypt(self, v:Union[str, bytes]) -> Union[str, bytes]:
        raise NotImplementedError