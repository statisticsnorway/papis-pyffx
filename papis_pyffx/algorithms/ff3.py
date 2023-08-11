import math
from .ffx import Feistel_cipher
from Crypto.Cipher import AES

class FF3(Feistel_cipher):
    #Implements the NIST standarddised round function FF3
    #Following the NIST example
    #https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-38g.pdf
    #https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/FF3samples.pdf
    tweak = bytes.fromhex('0000000000000000')

    def __init__(self, key, radix):
        super().__init__(key, radix)
        key = bytes(reversed(list(key)))
        self.cipherECB = AES.new(key, AES.MODE_ECB)
      
    @staticmethod
    def byte_xor(v1, v2):
        return bytes([_a ^ _b for _a, _b in zip(v1, v2)])
    
    @staticmethod
    def reverse_mask_64(by):
        x = int.from_bytes(by, 'big')
        x = ((x & 0x5555555555555555) << 1) | ((x & 0xAAAAAAAAAAAAAAAA) >> 1)
        x = ((x & 0x3333333333333333) << 2) | ((x & 0xCCCCCCCCCCCCCCCC) >> 2)
        x = ((x & 0x0F0F0F0F0F0F0F0F) << 4) | ((x & 0xF0F0F0F0F0F0F0F0) >> 4)
        x = ((x & 0x00FF00FF00FF00FF) << 8) | ((x & 0xFF00FF00FF00FF00) >> 8)
        x = ((x & 0x0000FFFF0000FFFF) << 16) | ((x & 0xFFFF0000FFFF0000) >> 16)
        x = ((x & 0x00000000FFFFFFFF) << 32) | ((x & 0xFFFFFFFF00000000) >> 32)
        return x.to_bytes(8, 'big')
    
    @staticmethod
    def reverse(by):
        by = list(by)
        by.reverse()
        return bytes(by)
       
    def _numRaxixX(self, X, reverse=False):
        x = 0
        if reverse:
            for i in range(len(X)):
                x = x*self.radix + X[len(X)-i-1]
        else:
            for i in range(len(X)):
                x = x*self.radix + X[i]
        return x
    
    def splitN(self, n, length):
        ret = list()
        for _ in range(length):
            ret.append(n % self.radix)
            n = n//self.radix
        ret.reverse()
        return ret
    
    def split(self, v):
        #Splits the list into two lists split at floor(len(v)/2)
        #FF1 uses floor, FF3 uses celing
        s = int((len(v)+1) //2)
        return v[:s], v[s:]
    
    def setP(self, W, i, B):
        p = [0]*16
        p[0:4] = list(W)
        p[3] = p[3] ^ i
        numRadixB = self._numRaxixX(B, reverse=True)
        numRadixB = numRadixB % (256**12)
        p[4:16] = list(numRadixB.to_bytes(12, byteorder='big'))
        return p
    
    def setS(self, p):
        #int.from_bytes(bytes, byteorder='little')
        return bytes(reversed(list(self.cipherECB.encrypt(bytes(reversed(list(p)))))))
    
    def encrypt(self, v, tweak = None):
        if not tweak:
            tweak = self.tweak
        if len(tweak) != 8:
            raise ValueError('Tweak not 64-bit')
            
        T = [tweak[0:4], tweak[4:8]]
        A, B = self.split(v)
        #print (A, B, T[0].hex(), T[1].hex())

        for i in range(8):
            #print(f'Round {i}')
            P = self.setP(T[(i+1)%2], i, B)
            S = self.setS(bytes(P))
            #print(P, S.hex())
            y = int.from_bytes(bytes(S), byteorder='big')
            m = (len(v)+(i+1)%2)//2
            c = (self._numRaxixX(A, True) + y)%(self.radix ** m)
            C = self.splitN(c, m)
            C.reverse()
            #print (y, c, C)
            A, B = B, C
            #print('A B', A, B)
        return A + B

    def decrypt(self, v, tweak = []):
        if not tweak:
            tweak = self.tweak
        if len(tweak) != 8:
            raise ValueError('Tweak not 64-bit')
            
        T = [tweak[0:4], tweak[4:8]]
        A, B = self.split(v)
        #print (A, B, T[0].hex(), T[1].hex())

        for i in range(7,-1,-1):
            #print(f'Round {i}')
            P = self.setP(T[(i+1)%2], i, A)
            S = self.setS(bytes(P))
            #print(P, S.hex())
            y = int.from_bytes(bytes(S), byteorder='big')
            m = (len(v)+(i+1)%2)//2
            c = (self._numRaxixX(B, True) - y)%(self.radix ** m)
            C = self.splitN(c, m)
            C.reverse()
            #print (y, c, C)
            A, B = C, A
            #print('A B', A, B)
        return A + B

    def add(self, a, b):
        raise NotImplementedError()

    def sub(self, a, b):
        raise NotImplementedError()
    
    def round(self, i, s, msg_length, tweak):
        #Subclasses must implement the round function and handle keys
        #i is the round number, s is the round input string, msg_length is the
        #length of the message, tweak is the tweak
        raise NotImplementedError()
        
