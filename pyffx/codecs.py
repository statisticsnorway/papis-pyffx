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
        if not len(v): raise ValueError('Cannot encrypt empty set')
        return self.unpack(self.ffx.encrypt(self.pack(v)), type(v))

    def decrypt(self, v):
        #Decrypts the variable v
        if not len(v): raise ValueError('Cannot decrypt empty set')
        return self.unpack(self.ffx.decrypt(self.pack(v)), type(v))

    @abc.abstractmethod
    def pack(self, v):
        #Transforms the object v into a list of integers based on the alphabet
        #If the alphabet is "abc" then "aac" transforms to [0,0,2]
        raise NotImplementedError()

    def unpack(self, v, t):
        #Transforms a list of integers (v) into an object of type t
        return t(self.alphabet[i] for i in v)


class String(Codec):
    def pack(self, v):
        try:
            return [self.pack_map[c] for c in v]
        except KeyError as e:
            raise ValueError('non-alphabet character: %s' % e)
            
    def unpack(self, v, t):
        return ''.join(super(String, self).unpack(v, list))

class Integer(String):
    def __init__(self, ffx, length=None, **kwargs):
        self.length = length
        super(Integer, self).__init__(ffx, string.digits, **kwargs)

    def pack(self, v):
        if self.length:
            return super(Integer, self).pack(str(v).zfill(self.length))
        else:
            return super(Integer, self).pack(str(v))

    def unpack(self, v, t):
        return int(super(Integer, self).unpack(v, t))
