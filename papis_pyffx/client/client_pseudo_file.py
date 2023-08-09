import requests
from typing import Iterable, Union
from papis_pyffx.protocol.workObject import WorkObject, FileTypes
from papis_pyffx.protocol.pseudoFileProtocol import PseudoFileProtocol, QUEUE_NAMES

class ClientPseudoFile(PseudoFileProtocol):
    def __init__(self, host : str, port : int, ssh = False):
        if not ssh:
            self.base_url = f'http://{host}:{str(port)}'
        else:
            self.base_url = f'https://{host}:{str(port)}'

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
