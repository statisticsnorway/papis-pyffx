import math
from .ffx import Feistel_cipher
from Crypto.Cipher import AES

class FF1(Feistel_cipher):
    #Implements the NIST standarddised round function FF1
    #Following the NIST example
    #https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-38g.pdf
    #https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/FF1samples.pdf  
    iv = bytes.fromhex('00000000000000000000000000000000')
    
    def __init__(self, key, radix):
        rounds = 10
        super().__init__(radix, rounds)
        self.key = key
        self.cipherECB = AES.new(self.key, AES.MODE_ECB)
        self.logRadix = math.log(radix, 2)
      
    @staticmethod
    def byte_xor(v1, v2):
        return bytes([_a ^ _b for _a, _b in zip(v1, v2)])
       
    def _numRaxixX(self, X):
        x = 0
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
    
    def setP(self, len_v, len_tweak):
        p = [1,2,1, 0,0,0, 10, 0, 0,0,0,0, 0,0,0,0]
        p[3:6] = list(self.radix.to_bytes(3, byteorder='big'))
        p[7] = len_v//2
        p[8:12] = list(len_v.to_bytes(4, byteorder='big'))
        p[12:16] = list(len_tweak.to_bytes(4, byteorder='big'))
        return p
    
    def setQ(self, tweak, i, B, b_var):
        numRadixB = self._numRaxixX(B)
        q = [0] * (16 + ((len(tweak) + 1 + b_var)//16) * 16)
        q[0:len(tweak)] = tweak
        q[-b_var-1] = i
        q[-b_var:] = list(numRadixB.to_bytes(b_var, byteorder='big'))
        return q
    
    def AES_CBC(self, plain):
        cipher = AES.new(self.key, AES.MODE_CBC, iv = self.iv)
        return cipher.encrypt(bytes(plain))[-16:]
    
    def setS(self, r, len_v):
        v_len = (len_v+1)//2
        d = 4*math.ceil(v_len*self.logRadix/32) + 4 #Equivalent to standard
        #print(f'd is {d}')
        if d<=16:
            return r[0:d]
        i = 0

        while d//16 != r//16:
            i += 1
            r = r + self.cipherECB.encrypt(
                self.byte_xor(r[0:16], i.to_bytes(16, byteorder='big')))   
        return r[0:d]
    
    def encrypt(self, v, tweak = []):
        A, B = self.split(v)
        b = math.ceil((len(v)+1)//2*self.logRadix/8)
        #print (A, B)
        P = self.setP(len(v),len(tweak))
        for i in range(10):
            #print(f'Round {i}')
            Q = self.setQ(tweak, i, B, b)
            R = self.AES_CBC(P + Q)
            #print(P, Q)
            s = self.setS(R, len(v))
            #print(bytes(s).hex())
            y = int.from_bytes(bytes(s), byteorder='big')
            m = (len(v)+i%2)//2
            c = (self._numRaxixX(A) + y)%(self.radix ** m)
            C = self.splitN(c, m)
            #print (s.hex(), y, c, C)
            A, B = B, C
            #print('A B', A, B)
            #c = self.add(a, self.round(i, b, len(v), tweak))
            #a, b = b, c
        return A + B
    
    def encrypt2(self, v, tweak = []):
        A, B = self.split(v)
        b = math.ceil((len(v)+1)//2*self.logRadix/8)
        #print (A, B)
        P = self.setP(len(v),len(tweak))
        for i in range(10):
            #print(f'Round {i}')
            Q = self.setQ(tweak, i, B, b)
            R = self.AES_CBC(P + Q)
            #print(P, Q)
            s = self.setS(R, len(v))
            #print(bytes(s).hex())
            y = int.from_bytes(bytes(s), byteorder='big')
            m = (len(v)+i%2)//2
            c = (self._numRaxixX(A) + y)%(self.radix ** m)
            C = self.splitN(c, m)
            #print (s.hex(), y, c, C)
            A, B = B, C
            #print('A B', A, B)
            #c = self.add(a, self.round(i, b, len(v), tweak))
            #a, b = b, c
        return A + B

    def decrypt(self, v, tweak = []):
        A, B = self.split(v)
        b = math.ceil((len(v)+1)//2*self.logRadix/8)
        #print (A, B)
        P = self.setP(len(v),len(tweak))
        for i in range(9,-1,-1):
            #print(f'Round {i}')
            Q = self.setQ(tweak, i, A, b)
            R = self.AES_CBC(P + Q)
            #print(P, Q)
            s = self.setS(R, len(v))
            #print(bytes(s).hex())
            y = int.from_bytes(bytes(s), byteorder='big')
            m = (len(v)+i%2)//2
            c = (self._numRaxixX(B) - y)%(self.radix ** m)
            C = self.splitN(c, m)
            #print (s.hex(), y, c, C)
            A, B = C, A
            #print('A B', A, B)
            #c = self.add(a, self.round(i, b, len(v), tweak))
            #a, b = b, c
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
        
