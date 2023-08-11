import requests
from typing import Iterable, Union, Callable
from papis_pyffx.protocol.workObject import WorkObject, FileTypes
from papis_pyffx.protocol.pseudoFileProtocol import PseudoFileProtocol, QUEUE_NAMES
from papis_pyffx.helper.reapeated_timer import RepeatedTimer

class ClientPseudoFile(PseudoFileProtocol):
    def __init__(self, host : str, port : int, ssh : bool = False, hookTimer : int = 10, startTimer = True):
        if not ssh:
            self.base_url = f'http://{host}:{str(port)}'
        else:
            self.base_url = f'https://{host}:{str(port)}'
        self._after_active_hook : list [Callable[[str, str, WorkObject],None]] = list()
        self._queues_stored : dict[str, list[WorkObject]] = None
        if startTimer:
            self._repeatTimer = RepeatedTimer(hookTimer, self._repeatTimerFunction)
        else:
            self._repeatTimer = None
    
    def close(self):
        if self._repeatTimer:
            self._repeatTimer.stop()

    def handle_http_exception(self, response : requests.Response):
        if response.status_code != 200:
            response.raise_for_status()

    def get_queues(self) -> dict[str, list[WorkObject]]:
        # Make a request to the server's get_queues endpoint
        response = requests.get(f'{self.base_url}/get_queues')
        self.handle_http_exception(response)
        # Process the response and return the result
        return {k : [WorkObject(**v) for v in li] for k, li in response.json().items()}
    
    def add(self, inn_file_name: str, out_file_name: str, pseudo_col: Iterable, file_type: Union[FileTypes, str], **kwargs) -> str:
        wo = WorkObject(inn_file_name = inn_file_name, out_file_name=out_file_name,pseudo_col=pseudo_col, file_type=file_type,**kwargs)
        return self.add_work(wo)
    
    def add_work(self, wo: WorkObject) -> str:
        # Make a request to the server's add_work endpoint
        response = requests.post(f'{self.base_url}/add_work', json=wo.asdict())
        self.handle_http_exception(response)
        # Process the response and return the result
        return response.text
       
    def remove_work(self, wo: WorkObject) -> str:
        # Make a request to the server's remove_work endpoint
        response = requests.post(f'{self.base_url}/remove_work', json=wo.asdict())
        self.handle_http_exception(response)
        # Process the response and return the result
        return response.text
    
    def register_after_active_hook(self, func : Callable[[str, str, WorkObject],None]) -> None:
        """Adds a callback after active (done or error) sending information back to the original sender. The callable takes 3 arguments 
        origin : str
        to : str
        work : Workobject
        Implementations must add either a flask blueprint to receive a callback or other methods to detect elements moved to finished.
        """
        self._after_active_hook.append(func)

    def _repeatTimerFunction(self):
        """Function run repeatably using the RepeatedTimer function to run it regularly"""
        if len(self._after_active_hook) == 0:
            return
        if self._queues_stored == None:
            self._queues_stored = self.get_queues()
            return
        queues = self.get_queues()
        newDone = set(queues[QUEUE_NAMES.DONE.value]) - set(self._queues_stored[QUEUE_NAMES.DONE.value])
        newError = set(queues[QUEUE_NAMES.ERROR.value]) - set(self._queues_stored[QUEUE_NAMES.ERROR.value])
        for newWork in newDone:
            for func in self._after_active_hook:
                func(QUEUE_NAMES.ACTIVE.value, QUEUE_NAMES.DONE.value, newWork)

        for newWork in newError:
            for func in self._after_active_hook:
                func(QUEUE_NAMES.ACTIVE.value, QUEUE_NAMES.ERROR.value, newWork)

        
