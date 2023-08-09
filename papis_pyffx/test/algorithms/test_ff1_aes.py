import unittest
from papis_pyffx.algorithms.ff1 import FF1

#FF1 NIST implementation https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-38g.pdf
#FF1 NIST test vectors https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/FF1samples.pdf

class FF1TestVectors(unittest.TestCase):
    key1 = bytes.fromhex('2B7E151628AED2A6ABF7158809CF4F3C')
    clear1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    tweak1 = list(bytes.fromhex('39383736353433323130'))
    chiffer1No = [2, 4, 3, 3, 4, 7, 7, 4, 8, 4]
    chiffer1Tw = [6, 1, 2, 4, 2, 0, 0, 7, 7, 3] 
    
    clear2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    tweak2 = list(bytes.fromhex('3737373770717273373737'))
    chiffer2 = [10, 9, 29, 31, 4, 0, 22, 21, 21, 9, 20, 13, 30, 5, 0, 9, 14, 30, 22] 
    
    key4 = bytes.fromhex('2B7E151628AED2A6ABF7158809CF4F3CEF4359D8D580AA4F')
    chiffer4No = [2, 8, 3, 0, 6, 6, 8, 1, 3, 2] 
    chiffer4Tw = [2, 4, 9, 6, 6, 5, 5, 5, 4, 9]
    chiffer6 = [33, 11, 19, 3, 20, 31, 3, 5, 19, 27, 10, 32, 33, 31, 3, 2, 34, 28, 27]
    
    key7 = bytes.fromhex('2B7E151628AED2A6ABF7158809CF4F3CEF4359D8D580AA4F7F036D6F04FC6A94')
    chiffer7No = [6, 6, 5, 7, 6, 6, 7, 0, 0, 9]
    chiffer7Tw = [1, 0, 0, 1, 6, 2, 3, 4, 6, 3]
    chiffer9 = [33, 28, 8, 10, 0, 10, 35, 17, 2, 10, 31, 34, 10, 21, 34, 35, 30, 32, 13]
    
    def test_FF1_128_NoTweak(self): #Sample #1
        cipher = FF1(self.key1, 10)
        self.assertEqual(cipher.encrypt(self.clear1), self.chiffer1No)
        self.assertEqual(cipher.decrypt(self.chiffer1No), self.clear1)
        
    def test_FF1_128_Tweak(self): #Sample #2
        cipher = FF1(self.key1, 10)
        self.assertEqual(cipher.encrypt(self.clear1, self.tweak1), self.chiffer1Tw)
        self.assertEqual(cipher.decrypt(self.chiffer1Tw, self.tweak1), self.clear1)
        
    def test_FF1_128_Tweak2(self): #Sample #3
        cipher = FF1(self.key1, 36)
        self.assertEqual(cipher.encrypt(self.clear2, self.tweak2), self.chiffer2)
        self.assertEqual(cipher.decrypt(self.chiffer2, self.tweak2), self.clear2)
        
    def test_FF1_192_NoTweak(self): #Sample #4
        cipher = FF1(self.key4, 10)
        self.assertEqual(cipher.encrypt(self.clear1), self.chiffer4No)
        self.assertEqual(cipher.decrypt(self.chiffer4No), self.clear1)      
        
    def test_FF1_192_Tweak(self): #Sample #5
        cipher = FF1(self.key4, 10)
        self.assertEqual(cipher.encrypt(self.clear1, self.tweak1), self.chiffer4Tw)
        self.assertEqual(cipher.decrypt(self.chiffer4Tw, self.tweak1), self.clear1)
        
    def test_FF1_192_Tweak2(self): #Sample #6
        cipher = FF1(self.key4, 36)
        self.assertEqual(cipher.encrypt(self.clear2, self.tweak2), self.chiffer6)
        self.assertEqual(cipher.decrypt(self.chiffer6, self.tweak2), self.clear2)

    def test_FF1_256_NoTweak(self): #Sample #7
        cipher = FF1(self.key7, 10)
        self.assertEqual(cipher.encrypt(self.clear1), self.chiffer7No)
        self.assertEqual(cipher.decrypt(self.chiffer7No), self.clear1)      
        
    def test_FF1_256_Tweak(self): #Sample #8
        cipher = FF1(self.key7, 10)
        self.assertEqual(cipher.encrypt(self.clear1, self.tweak1), self.chiffer7Tw)
        self.assertEqual(cipher.decrypt(self.chiffer7Tw, self.tweak1), self.clear1)
        
    def test_FF1_256_Tweak2(self): #Sample #9
        cipher = FF1(self.key7, 36)
        self.assertEqual(cipher.encrypt(self.clear2, self.tweak2), self.chiffer9)
        self.assertEqual(cipher.decrypt(self.chiffer9, self.tweak2), self.clear2)   