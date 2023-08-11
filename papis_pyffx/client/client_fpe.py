import requests
from papis_pyffx.protocol.fpeProtocol import FpeProtocol

class ClientFPE(FpeProtocol):
    def __init__(self, host : str, port : int, ssh = False):
        if not ssh:
            self.base_url = f'http://{host}:{str(port)}'
        else:
            self.base_url = f'https://{host}:{str(port)}'

    def handle_http_exception(self, response : requests.Response):
        if response.status_code != 200:
            response.raise_for_status()

    def encrypt(self, v : str) -> str:
        response = requests.get(f"{self.base_url}/encrypt/{v}")
        self.handle_http_exception(response)
        return response.text

    def decrypt(self, v : str) -> str:
        response = requests.get(f"{self.base_url}/decrypt/{v}")
        self.handle_http_exception(response)
        return response.text

    def encrypt_set(self, v : list[str]) -> dict[str, str]:
        response = requests.post(f"{self.base_url}/encrypt_set/", json=v)
        self.handle_http_exception(response)
        return response.json()

    def decrypt_set(self, v : list[str]) -> dict[str, str]:
        response = requests.post(f"{self.base_url}/decrypt_set/", json=v)
        self.handle_http_exception(response)
        return response.json()

    def max_query_size(self) -> int:
        response = requests.get(f"{self.base_url}/max_query_size")
        self.handle_http_exception(response)
        return int(response.text)

    def get_alphabet(self) -> str:
        response = requests.get(f"{self.base_url}/get_alphabet")
        self.handle_http_exception(response)
        return response.text
