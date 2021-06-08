import abc
import string
import six

from pyffx.ffx import FFX


@six.add_metaclass(abc.ABCMeta)
class Codec(object):
    #Abstract class 
    def __init__(self, ffx, alphabet, **kwargs):
        self.ffx = ( ffx 
            if hasattr(ffx, 'encrypt') and hasattr(ffx, 'decrypt') 
            else FFX(ffx, len(alphabet), **kwargs) )
        self.alphabet = alphabet
        self.pack_map = {c: i for i, c in enumerate(alphabet)}

    def encrypt(self, v):
        #Encrypts the variable v
        return self.unpack(self.ffx.encrypt(self.pack(v)))

    def decrypt(self, v):
        #Decrypts the variable v
        return self.unpack(self.ffx.decrypt(self.pack(v)))

    @abc.abstractmethod
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
        return ''.join(super(String, self).unpack(v))

class Integer(String):
    def __init__(self, ffx, length, **kwargs):
        self.length = length
        super(Integer, self).__init__(ffx, string.digits, **kwargs)

    def pack(self, v):
        return super(Integer, self).pack(str(v).zfill(self.length))

    def unpack(self, v):
        return int(super(Integer, self).unpack(v))
