from abc import ABC, abstractmethod

class Feistel_cipher(ABC):
    #Abstract class implementing unbalanced Feistel cipher according to 
    #http://csrc.nist.gov/groups/ST/toolkit/BCM/documents/proposedmodes/ffx/ffx-spec.pdf (using Figure 1, method 2)
    #Same Feistel in https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-38Gr1-draft.pdf

    def __init__(self, radix, rounds):
        self.radix = radix
        self.rounds = rounds

    @abstractmethod
    def add(self, a, b):
        raise NotImplementedError()

    @abstractmethod
    def sub(self, a, b):
        raise NotImplementedError()
    
    @abstractmethod
    def round(self, i, s, msg_length, tweak):
        #Subclasses must implement the round function and handle keys
        #i is the round number, s is the round input string, msg_length is the
        #length of the message, tweak is the tweak
        raise NotImplementedError()
        
        
    def split(self, v):
        #Splits the list into two lists split at floor(len(v)/2)
        #FF1 uses floor, FF3 uses celing
        s = int(len(v) / 2)
        return v[:s], v[s:]

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
