from typing import Protocol, Iterable
from papis_pyffx.protocol.algProtocol import AlgProtocol

class FpeProtocol(AlgProtocol):
    """Extends the simple algorithm protocol that has only encrypt and decrypt
    with a encrypt/decrypt set up to size maxQuerySize and alphabet used by the FPE encyption algorithm
    """
    def encrypt_set(self, di : Iterable[str] ) -> dict[str, str]:
        """Encrypts an iterable element of type strings.
        Returns:
            A dictionary containing the original string as key and the encrypted string as value."""
        raise NotImplementedError
    
    def decrypt_set(self, di : Iterable[str]) -> dict[str, str]:
        """Decrypts an iterable element of type strings.
        Returns:
            A dictionary containing the original string as key and the decrypted string as value."""
        raise NotImplementedError

    def max_query_size(self) -> int:
        """Returns:
            A integer indicating the maximum size of the iterable transmitted to an encryptSet/decryptSet"""
        raise NotImplementedError
    
    def get_alphabet(self) -> str:
        """Returns:
            A string indicating set of the allowed alphabet used by the algorithm."""
        raise NotImplementedError