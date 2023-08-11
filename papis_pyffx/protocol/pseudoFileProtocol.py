from enum import Enum
from typing import Protocol, Iterable, Union, Callable

from papis_pyffx.protocol.workObject import WorkObject, FileTypes

class QUEUE_NAMES(Enum):
    ACTIVE = 'active'
    QUEUE = 'queue'
    DONE = 'done'
    ERROR = 'error'

    @classmethod
    def values(cls):
        return tuple(map(lambda c: c.value, cls))

class PseudoFileProtocol(Protocol):
    """Protocol for PseudoService a service to perform pseudonymisation. Handling users can be achived by inheriting from UserProtocol
      Service only accepts work objects and puts them into queues, and returns status of queues. 
        """
    def get_queues(self) -> dict[str, list[WorkObject]]:
        """Gets info on queues in pseudoService.
            Returns queue name and list of WorkObjects"""
        raise NotImplementedError
    
    def add(self, inn_file_name : str, out_file_name : str, pseudo_col : Iterable, file_type : Union[FileTypes, str], **kwargs) -> str:
        """Adds a WorkObject based on minimal information supplied. Accepts kwargs for other data
            Returns a string with inn_file_name if all is ok, otherwise returns error message."""
        raise NotImplementedError
    
    def add_work(self, wo : WorkObject) -> str:
        """Adds a WorkObject based on the WorkObject element.
            Returns a string with inn_file_name if all is ok, otherwise returns error message."""
        raise NotImplementedError
       
    def remove_work(self, wo : WorkObject) -> str:
        """Removes a WorkObject based on the WorkObject element, only inn_file_name, out_file_name, pseudo_col and user has to match
            Returns a string with inn_file_name if all is ok, otherwise returns error message."""
        raise NotImplementedError
    
    def register_after_active_hook(self, func : Callable[[str, str, WorkObject],None]) -> None:
        """Adds a callback after active (done or error) sending information back to the original sender. The callable takes 3 arguments 
        origin : str
        to : str
        work : Workobject
        Implementations must add either a flask blueprint to receive a callback or other methods to detect elements moved to finished.
        """
        raise NotImplementedError
