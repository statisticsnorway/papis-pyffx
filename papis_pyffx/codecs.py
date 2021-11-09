from abc import ABC, abstractmethod
import string

class Codec(ABC):
    #Abstract class 
    def __init__(self, ffx, key, alphabet, **kwargs):
        if not hasattr(ffx, 'encrypt') and hasattr(ffx, 'decrypt'):
            raise ValueError('No cipher supplied')
        self.ffx = ffx(key, len(alphabet))
        self.alphabet = alphabet
        self.pack_map = {c: i for i, c in enumerate(alphabet)}

    def encrypt(self, v):
        #Encrypts the variable v
        return self.unpack(self.ffx.encrypt(self.pack(v)))

    def decrypt(self, v):
        #Decrypts the variable v
        return self.unpack(self.ffx.decrypt(self.pack(v)))

    @abstractmethod
    def pack(self, v):
        #Transforms the object v into a list of integers based on the alphabet
        #If the alphabet is "abc" then "aac" transforms to [0,0,2]
        raise NotImplementedError()

    def unpack(self, v):
        #Transforms a list of integers (v) into an list of elements in the alphabet
        return [self.alphabet[i] for i in v]


class String(Codec):
    def pack(self, v):
        try:
            return [self.pack_map[c] for c in v]
        except KeyError as e:
            raise ValueError('non-alphabet character: %s' % e)
            
    def unpack(self, v):
        return ''.join(super().unpack(v))

class Integer(String):
    def __init__(self, ffx, key, length, **kwargs):
        self.length = length
        super().__init__(ffx, key, string.digits, **kwargs)

    def pack(self, v):
        return super().pack(str(v).zfill(self.length))

    def unpack(self, v):
        return int(super().unpack(v))
