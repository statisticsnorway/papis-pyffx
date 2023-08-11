import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from papis_pyffx.protocol.userProtocol import UserProtocol


class ClientUser(UserProtocol):
    def __init__(self, host : str, port : int, ssh = False):
        if not ssh:
            self.base_url = f'http://{host}:{str(port)}'
        else:
            self.base_url = f'https://{host}:{str(port)}'

    def handle_http_exception(self, response : requests.Response):
        if response.status_code != 200:
            response.raise_for_status()
        
    def login_user(self, user_name : str, password : str, encrypted : bool) -> str:
        # Make a request to the server's login endpoint. user_name and password is sent in the clear to the function.
        # Returns user_name if ok
        if encrypted:
            key = self.get_public_key()
            imported_key = RSA.import_key(key.encode())
            cipher = PKCS1_v1_5.new(imported_key)
            password = cipher.encrypt(password.encode())

        response = requests.post(f'{self.base_url}/login_user', json={'user_name': user_name, 'password': password,
                                                                        'encrypted': encrypted})
        self.handle_http_exception(response)
        return response.text
    
    def logout_user(self, user_name: str) -> str:
        # Make a request to the server's logout endpoint. Returns user_name if ok
        response = requests.get(f'{self.base_url}/logout/{user_name}')
        self.handle_http_exception(response)
        # Process the response and return the result
        return response.text
    
    def keep_alive(self, user_name: str) -> str:
        # Keeps the user logged in otherwise the user might be logged out if a timeout happens. Returns 'True' if ok
        response = requests.get(f'{self.base_url}/keep_alive/{user_name}')
        self.handle_http_exception(response)
        return response.text
    
    def get_public_key(self) -> str:
        """Returns the public key user for encrypting the password used for login_user"""
        response = requests.get(f'{self.base_url}/get_public_key/')
        self.handle_http_exception(response)
        return response.text
    
    def get_hash_salt(self) -> str:
        # Gets the salt used for hashing, returns the salt as a string.
        response = requests.get(f'{self.base_url}/get_hash_salt/')
        self.handle_http_exception(response)
        return response.text
