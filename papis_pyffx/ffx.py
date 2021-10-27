import hashlib
import hmac
import math
import struct
from abc import ABC, abstractmethod

DEFAULT_ROUNDS = 10


class Feistel_cipher(ABC):
    #Abstract class implementing unbalanced Feistel cipher according to 
    #http://csrc.nist.gov/groups/ST/toolkit/BCM/documents/proposedmodes/ffx/ffx-spec.pdf (using Figure 1, method 2)
    #Same Feistel in https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-38Gr1-draft.pdf

    def __init__(self, radix, rounds):
        self.radix = radix
        self.rounds = rounds

    def add(self, a, b):
        #Adds a and b, Note: Characterwise addition
        return [(a_i + b_i) % self.radix for a_i, b_i in zip(a, b)]

    def sub(self, a, b):
        #Subtracts b from a, Note: Characterwise subtraction
        return [(a_i - b_i) % self.radix for a_i, b_i in zip(a, b)]

    def split(self, v):
        #Splits the list into two lists split at floor(len(v)/2)
        #FF1 uses floor, FF3 uses celing
        s = int(len(v) / 2)
        return v[:s], v[s:]
    
    @abstractmethod
    def round(self, i, s, msg_length, tweak):
        #Subclasses must implement the round function and handle keys
        #i is the round number, s is the round input string, msg_length is the
        #length of the message, tweak is the tweak
        raise NotImplementedError()

    def encrypt(self, v, tweak = None):
        a, b = self.split(v)
        for i in range(self.rounds):
            c = self.add(a, self.round(i, b, len(v), tweak))
            a, b = b, c
        return a + b

    def decrypt(self, v, tweak = None):
        a, b = self.split(v)
        for i in range(self.rounds - 1, -1, -1):
            b, c = a, b
            a = self.sub(c, self.round(i, b, len(v), tweak))
        return a + b

class FFX(Feistel_cipher):
    #Implements the round function F as a SHA1 run through 
    #a hmac function (Keyed-hashing for message authentication)
    #to generate a stream of random values (modulo radix.)
    def __init__(self, key, radix, rounds=DEFAULT_ROUNDS, digestmod=hashlib.sha1):
        self.key = key
        self.digestmod = digestmod
        self.digest_size = self.digestmod().digest_size
        super().__init__(radix, rounds)
        
    def round(self, i, s, msg_length, tweak = None):
        #Implements the round function
        #message length is ignored.
        s = s if not tweak else s + tweak
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
            

