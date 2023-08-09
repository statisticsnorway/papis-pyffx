from typing import Protocol, Iterable, Union
from papis_pyffx.protocol.workObject import WorkObject, FileTypes

QUEUE_NAMES = ('active','queue','done','error')

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
