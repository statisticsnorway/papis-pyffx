import hashlib
import hmac
import math
import struct
import six
import abc

DEFAULT_ROUNDS = 10

@six.add_metaclass(abc.ABCMeta)
class Feistel_cipher(object):
    #Abstract class implementing unbalanced Feistel cipher 
    #Input and outputs are lists of nonezero length
    def __init__(self, radix, rounds):
        self.radix = radix
        self.rounds = rounds

    def add(self, a, b):
        #Adds a and b, Note: a and b must be of equal length
        return [(a_i + b_i) % self.radix for a_i, b_i in zip(a, b)]

    def sub(self, a, b):
        #Subtracts b from a, Note: a and b must be of equal length
        return [(a_i - b_i) % self.radix for a_i, b_i in zip(a, b)]

    def split(self, v):
        #Splits the list into two lists split at floor(len(v)/2)
        s = int(len(v) / 2)
        return v[:s], v[s:]
    
    @abc.abstractmethod
    def round(self, i, s, length_of_split):
        #Subclasses must implement the round function
        raise NotImplementedError()

    def encrypt(self, v):
        a, b = self.split(v)
        for i in range(self.rounds):
            c = self.add(a, self.round(i, b, len(v)))
            a, b = b, c
        return a + b

    def decrypt(self, v):
        a, b = self.split(v)
        for i in range(self.rounds - 1, -1, -1):
            b, c = a, b
            a = self.sub(c, self.round(i, b, len(v)))
        return a + b

class FFX(Feistel_cipher):
    #Implements the Feustel cipher according to
    #http://csrc.nist.gov/groups/ST/toolkit/BCM/documents/proposedmodes/ffx/ffx-spec.pdf
    #Defaults to hashlib as pseudorandom function
    def __init__(self, key, radix, rounds=DEFAULT_ROUNDS, digestmod=hashlib.sha1):
        self.key = key
        self.digestmod = digestmod
        self.digest_size = self.digestmod().digest_size
        super(FFX, self).__init__(radix, rounds)
        
    def round(self, i, s, length_of_split):
        #Implements the round function, i is the round number, 
        #s is the round input and 
        key = struct.pack('I%sI' % len(s), i, *s)
        chars_per_hash = int(self.digest_size * math.log(256, self.radix))
        i = 0
        while True:
            h = hmac.new(self.key, key + struct.pack('I', i), self.digestmod)
            d = int(h.hexdigest(), 16)
            for _ in range(chars_per_hash):
                d, r = divmod(d, self.radix)
                yield r
            key = h.digest()
            i += 1
            

