from Crypto.Random import get_random_bytes
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from papis_pyffx.protocol.userProtocol import UserProtocol
from papis_pyffx.helper.crypto_rsa import CryptoRSA

@dataclass
class _MockUser:
    user_name : str #user_name
    password : str #password
    touched : datetime = field(default_factory= datetime.now)

class MockUsers(UserProtocol):
    """Mocks the login, logout, keepalive, keep_alive_time is in seconds. Uses CryptoRSA for cryptographic operations.
    """
    def __init__(self, keep_alive_time : int) -> None:
        super().__init__()
        self.rsa = CryptoRSA()
        self.hash_salt = get_random_bytes(32).hex()
        self.keep_alive_time = timedelta(seconds=keep_alive_time)
        self.user_dict : dict[str, _MockUser] = dict()

    def _is_timed_out(self, user : _MockUser) -> bool:
        return (datetime.now() - user.touched) > self.keep_alive_time
    
    def login_user(self, user_name : str, password : str, encrypted : bool) -> str:
        """Logs inn user usering user_name and password, 
            If encrypted is set to true then password is encrypted using the key from get_public_key
            If encrypted is set to false then password is sent in the clear.
            Returns a string with user_name if all is ok, otherwise returns error message.
        """
        if encrypted:
            clear = self.cipher_decoder(password, None, 0)
            if clear == None:
                raise ValueError('Could not decrypt password')
        else:
            clear = password
        self.user_dict[user_name] = _MockUser(user_name, clear)
        return user_name
    
    def logout_user(self, user_name: str) -> str:
        """Logs out user.
            Returns a string with user_name if all is ok, None if could not decrypt otherwise returns error message."""
        return self.user_dict.pop(user_name, None)
    
    def keep_alive(self, user_name : str) -> str:
        """Keeps the user logged in otherwise the user might be logged out if a timeout happens. 
            user_hash is a combination of username, password and salt
            Returns a string with user_name if all is ok, None if does not exist"""
        user = self.user_dict.get(user_name, None)
        if user == None:
            return None
        elif self._is_timed_out(user):
            del self.user_dict[user_name]
            return None
        else:
            user.touched = datetime.now()
    
    def get_public_key(self) -> str:
        return self.rsa.export_public_key()
    
    def get_hash_salt(self) -> str:
        return self.get_hash_salt