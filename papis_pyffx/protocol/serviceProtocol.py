from typing import Protocol, Iterable
from papis_pyffx.protocol.fpeProtocol import FpeProtocol
from papis_pyffx.protocol.workObject import WorkObject

class PseudoService(Protocol):
    def __init__(cryptoService : FpeProtocol, loggingPath : str = None, sleepInterval : int = 0.1) -> None:
        raise NotImplementedError
    
    def close() -> None:
        raise NotImplementedError

    def login_user(username : str, password : str) -> str:
        raise NotImplementedError
    
    def logout(username: str) -> str:
        raise NotImplementedError
    
    def keepAlive(username : str, userHash : str) -> None:
        raise NotImplementedError
    
    def getQueues() -> dict[str, WorkObject]:
        raise NotImplementedError
       
    def getInfo(showtables : list[bool]) -> list[tuple[str]]:
        raise NotImplementedError
    
    def addWork(wo : WorkObject) -> str:
        raise NotImplementedError
       
    def add(self, innFileName : str, outFileName : str, pseudoCol : Iterable, filetype : str, **kwargs) -> str:
        raise NotImplementedError
    
    def remove(wo : WorkObject) -> str:
        raise NotImplementedError
    
    def encryptSet(clearSet : Iterable[str]) -> dict[str, str]:
        raise NotImplementedError
    
    def encryptSet(chifferSet : Iterable[str]) -> dict[str, str]:
        raise NotImplementedError