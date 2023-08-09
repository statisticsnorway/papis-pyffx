from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
"""Helper functions for generating RSA keys, exporting public key, encrypting with public key and decrpyting.
"""
"""Mock code for encryption,
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        #Key generation and export public key
        rsaKey = RSA.generate(keylength)
        export_key = rsaKey.public_key().export_key('PEM').decode()
        #Code for import public key and encryption of text
        imp = RSA.import_key(export_key.encode())
        cipher = PKCS1_v1_5.new(imp)
        ciphertext = cipher.encrypt('Ken sent me'.encode())
        #Code for deccryption of text
        cipherdecoder = PKCS1_v1_5.new(key)
        clear = cipherdecoder.decrypt(ciphertext,None,0).decode()
        print(clear) #Returns 'Ken sent me' """
    
class CryptoRSA:
    """Helper class for creating RSA keys and sending encrypted keys"""
    def __init__(self, keylength : int = 4096) -> None:
        self.rsaKey = RSA.generate(keylength)
        self.cipher_decoder = PKCS1_v1_5.new(self.rsaKey)

    def export_public_key(self) -> str:
        """Exports the public key as a string.
            Key is exported using the PEM format using standard utf-8 encoding of bytes"""
        return self.rsaKey.public_key().export_key('PEM').decode()
    
    @classmethod
    def encrypt_data(cls, data : str, public_key : str):
        """Encrypts data using the public key. Assumes standard utf-8 encoding of text to bytes and of public key.
            Returns the encrypted text as binary in hex"""
        imported_public_key = RSA.import_key(public_key.encode())
        cipher = PKCS1_v1_5.new(imported_public_key)
        return cipher.encrypt(data.encode()).hex()
    
    def decrypt_data(self, data : str):
        """Decrypts data using the private key. Assumes data is binary data in hex, and the text is
        text encoded from bytes using utf-8. If data cannot be decoded returns None"""
        clear = self.cipher_decoder.decrypt(bytes.fromhex(data), None, 0)
        if not clear:
            return None
        else:
            return clear.decode()