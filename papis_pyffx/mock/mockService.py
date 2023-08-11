from datetime import datetime, timedelta
from typing import Iterable, Union
from random import random

from papis_pyffx.protocol.pseudoFileProtocol import PseudoFileProtocol, QUEUE_NAMES
from papis_pyffx.protocol.workObject import WorkObject, FileTypes
from papis_pyffx.mock.mockUsers import MockUsers

class MockPseudoFile(PseudoFileProtocol):
    """Mock for ServiceProtocol is a mock for a service to perform pseudonymisation. Also imports a mock for handling users
      Service only accepts work objects and puts them into queues, and returns status of queues. 
      User handling is performed by the MockUsers class which is inherited into the MockServices
        """
    
    def __init__(self, keep_alive_time: int, handling_time : int) -> None:
        super().__init__(keep_alive_time)
        self.handling_time = handling_time
        self.active : list[WorkObject] = list()
        self.queue : list[WorkObject]= list()
        self.done : list[WorkObject]= list()
        self.error : list[WorkObject]= list()
        for queue in QUEUE_NAMES:
            if not hasattr(self, queue):
                raise AttributeError(f'__init__ is missing queue {queue}')

    def get_queues(self) -> dict[str, list[WorkObject]]:
        """Gets info on queues in pseudoService.
            Returns queue name and list of WorkObjects"""
        self._runQueues()
        return {queue : getattr(self, queue).copy() for queue in QUEUE_NAMES}
    
    def add(self, inn_file_name : str, out_file_name : str, pseudo_col : Iterable, file_type : Union[FileTypes, str], **kwargs) -> str:
        """Adds a WorkObject based on minimal information supplied. Accepts kwargs for other data
            Returns a string with inn_file_name if all is ok, otherwise returns error message."""
        wo = WorkObject(inn_file_name = inn_file_name, out_file_name=out_file_name,pseudo_col=pseudo_col, file_type=file_type,**kwargs)
        return self.add_work(wo)
    
    def add_work(self, wo : WorkObject) -> str:
        """Adds a WorkObject based on the WorkObject element.
            Returns a string with inn_file_name if all is ok, otherwise returns error message."""
        if wo in self.queue:
            index = self.queue.index(wo)
            self.queue[index] = wo.touch()
        else:
            self.queue.append(wo.touch())
        return wo.inn_file_name
       
    def remove_work(self, wo : WorkObject) -> str:
        """Removes a WorkObject based on the WorkObject element, only inn_file_name, out_file_name, pseudo_col and user has to match
            Returns a string with inn_file_name if all is ok, otherwise returns error message."""
        if wo in self.queue:
            self.queue.remove(wo)
            return wo.inn_file_name
        else:
            return None
    
    def _runQueues(self):
        send_to_error_percent = 0.1
        while self.active:
            self.queue.insert(0, self.active.pop())
        deletequeue : list[WorkObject] = list()
        for wo in tuple(self.queue): 
            if datetime.now - wo.timing > timedelta(self.handling_time):
                deletequeue.append(wo)
                self.queue.remove(wo)
            