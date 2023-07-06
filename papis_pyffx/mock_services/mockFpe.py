from papis_pyffx.fixedalphabet import FixedAlphabet
from papis_pyffx.protocol.fpeProtocol import FpeProtocol
from papis_pyffx.ff3 import FF3
from string import ascii_letters, digits
from typing import Protocol, Union
from enum import Enum
from threading import Lock

class OPERATIONS(Enum):
    encrypt = 'encrypt'
    decrypt = 'decrypt'

class AlgProtocol(Protocol):
    def encrypt(self, v : str) -> str:
        raise NotImplementedError

    def decrypt(self, v : str) -> str:
        raise NotImplementedError
    
    def filter(self, v) -> Union[bytes, str]:
        raise NotImplementedError
    
    def unfilter(self, orig : str, pseudo : bytes) -> str:
        raise NotImplementedError

def _algorithm(key : str = 'EF4359D8D580AA4F7F036D6F04FC6A94', algorithm = FF3):
    key = bytes.fromhex(key)
    alphabet = ascii_letters + digits
    alg = FixedAlphabet(algorithm, key, alphabet = alphabet)
    #from ff3 import FF3Cipher 
    #alg = FF3Cipher(key=key, tweak='0'*16, radix=62)
    return alg
    
class MockFpe(FpeProtocol):
    def __init__(self, algorithm : AlgProtocol = _algorithm(), maxQuerySize : int = 10000):
        self.algorithm = algorithm
        self.lock = Lock()
        self.maxSize = maxQuerySize

    def encrypt(self, clear: str) -> str:
        di = self._getCrypt(set((clear,)), OPERATIONS.encrypt)
        return di[clear]
        
    def decrypt(self, chiffer : str) -> str:
        di = self._getCrypt(set((chiffer,)), OPERATIONS.decrypt)
        return di[chiffer]

    def encryptSet(self, clearSet) -> dict:
        return self._getCrypt(clearSet, OPERATIONS.encrypt)

    def decryptSet(self, chifferSet) -> dict:
        return self._getCrypt(chifferSet, OPERATIONS.decrypt)
    
    def maxQuerySize(self) -> int:
        return self.maxSize
            
    def _getCrypt(self, chSet : Union[set, list], op : OPERATIONS) -> dict:
        #Ensures all elements of chSet are of type str                
        initialDict = {x : self.algorithm.filter(str(x)) for x in chSet}
        strSet = set(initialDict.values()) - {''}
        #Checks database for matches otherwise computes from algorithm
        #Inserts missing matches into database
        with self.lock: #Ensures multithreading works 
            cryptFunc = getattr(self.algorithm, op.value)
            matchesDict = {x : cryptFunc(x) for x in strSet}
        
        #Return set with original elements
        matchesDict[''] = ''
        return {k : self.algorithm.unfilter(k, matchesDict[v]) for k, v in initialDict.items()}

