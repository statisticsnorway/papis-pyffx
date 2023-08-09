import hashlib
import hmac
import math
import struct
from .feistel_abs import Feistel_cipher

DEFAULT_ROUNDS = 10

class FFX(Feistel_cipher):
    #Implements the round function F as a SHA1 run through 
    #a hmac function (Keyed-hashing for message authentication)
    #to generate a stream of random values (modulo radix.)
    def __init__(self, key, radix, digestmod=hashlib.sha1):
        self.key = key
        self.digestmod = digestmod
        self.rounds = DEFAULT_ROUNDS
        self.digest_size = self.digestmod().digest_size
        super().__init__(key, radix)
    
    def add(self, a, b):
        #Adds a and b, Note: Characterwise addition
        return [(a_i + b_i) % self.radix for a_i, b_i in zip(a, b)]

    def sub(self, a, b):
        #Subtracts b from a, Note: Characterwise subtraction
        return [(a_i - b_i) % self.radix for a_i, b_i in zip(a, b)]
    
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
            

