from typing import Protocol

class AlgProtocol(Protocol):
    """Basic protocol that any FPE (Format-preserving encryption) algorithm must adhere to.
    Formatpreserving encrytion algorithms takes strings as input other algorithms take bytes as input.
    """
    def encrypt(self, v : str) -> str:
        """Encrypts v returns same type as input"""
        raise NotImplementedError

    def decrypt(self, v : str) -> str:
        """Decrypts v returns same type as input"""
        raise NotImplementedError