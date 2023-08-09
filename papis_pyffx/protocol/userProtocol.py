from typing import Protocol

class UserProtocol(Protocol):
    """Protocol for handling users: login, logout, keep_alive
        users password are secured using userHash which is a combination of username, password and salt
        host and port is not transmitted over this interface and is implisit agreed on."""

    """Code for encryption, 'k' is exported used get_public_key() function:
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        #Code for encryption
        imp = RSA.import_key(k.encode())
        cipher = PKCS1_v1_5.new(imp)
        ciphertext = cipher.encrypt('Ken sent me'.encode())
        #Code for deccryption
        cipherdecoder = PKCS1_v1_5.new(key)
        clear = cipherdecoder.decrypt(ciphertext,None,0).decode()
        print(clear) #Returns 'Ken sent me' """
    
    def login_user(self, user_name : str, password : str, encrypted : bool) -> str:
        """Logs inn user usering user_name and password, user_name and password is sent in the clear to the function.
            If encrypted is set to true then password is encrypted using the key from get_public_key before the data is sent, 
            If encrypted is set to false then password is sent in the clear.
            Returns a string with user_name if all is ok, otherwise returns error message."""
        raise NotImplementedError
    
    def logout_user(self, user_name: str) -> str:
        """Logs out user user_hash is a combination of username, password and salt
            Returns a string with user_name if all is ok, otherwise returns error message."""
        raise NotImplementedError
    
    def keep_alive(self, user_name : str) -> str:
        """Keeps the user logged in otherwise the user might be logged out if a timeout happens. 
            user_hash is a combination of username, password and salt
            Returns a string with user_name if all is ok, otherwise returns error message."""
        raise NotImplementedError
    
    def get_public_key(self) -> str:
        """Returns the public key user for encrypting the password used for password element in login_user
        from Crypto.PublicKey import RSA
        key = RSA.generate(4096)
        k = key.public_key().export_key('PEM').decode()
        k is returned"""
        raise NotImplementedError
    
    def get_hash_salt(self) -> str:
        """Gets the salt used for hashing, returns the salt as a string.
            from Crypto.Random import get_random_bytes
            return get_random_bytes(32).hex()
            Returns a string that is used in workObject function get_user_hash(username : str, pw : str, secretVal : str)"""
        raise NotImplementedError

