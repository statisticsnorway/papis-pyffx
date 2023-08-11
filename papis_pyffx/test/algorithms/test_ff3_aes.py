import unittest
from papis_pyffx.algorithms.ff3 import FF3

#FF3 NIST implementation https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-38g.pdf
#FF3 NIST test vectors https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/FF3samples.pdf

class FF3TestVectors(unittest.TestCase):
    key1 = bytes.fromhex('EF4359D8D580AA4F7F036D6F04FC6A94')
    clear1 = [8, 9, 0, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0]
    tweak1 = list(bytes.fromhex('D8E7920AFA330A73'))
    tweak2 = list(bytes.fromhex('9A768A92F60E12D8'))
    chiffer1 = [7, 5, 0, 9, 1, 8, 8, 1, 4, 0, 5, 8, 6, 5, 4, 6, 0, 7]
    chiffer2 = [0, 1, 8, 9, 8, 9, 8, 3, 9, 1, 8, 9, 3, 9, 5, 3, 8, 4]

    clear3 = [8, 9, 0, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 7, 8, 9, 0, 0, 0, 0, 0, 0]
    chiffer3 = [4, 8, 5, 9, 8, 3, 6, 7, 1, 6, 2, 2, 5, 2, 5, 6, 9, 6, 2, 9, 3, 9, 7, 4, 1, 6, 2, 2, 6]
    tweak4 = list(bytes.fromhex('0000000000000000'))
    chiffer4 = [3, 4, 6, 9, 5, 2, 2, 4, 8, 2, 1, 7, 3, 4, 5, 3, 5, 1, 2, 2, 6, 1, 3, 7, 0, 1, 4, 3, 4]
    
    clear5 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    chiffer5 = [16, 2, 25, 20, 4, 0, 18, 9, 9, 2, 15, 23, 2, 0, 12, 19, 10, 20, 11]
    
    key6 = bytes.fromhex('EF4359D8D580AA4F7F036D6F04FC6A942B7E151628AED2A6')
    chiffer6 = [6, 4, 6, 9, 6, 5, 3, 9, 3, 8, 7, 5, 0, 2, 8, 7, 5, 5]
    chiffer7 = [9, 6, 1, 6, 1, 0, 5, 1, 4, 4, 9, 1, 4, 2, 4, 4, 4, 6]
    chiffer8 = [5, 3, 0, 4, 8, 8, 8, 4, 0, 6, 5, 3, 5, 0, 2, 0, 4, 5, 4, 1, 7, 8, 6, 3, 8, 0, 8, 0, 7]
    chiffer9 = [9, 8, 0, 8, 3, 8, 0, 2, 6, 7, 8, 8, 2, 0, 3, 8, 9, 2, 9, 5, 0, 4, 1, 4, 8, 3, 5, 1, 2]
    chiffer10 = [18, 0, 18, 17, 14, 2, 19, 15, 19, 7, 10, 9, 24, 25, 15, 9, 25, 8, 8]
    
    
    key11 = bytes.fromhex('EF4359D8D580AA4F7F036D6F04FC6A942B7E151628AED2A6ABF7158809CF4F3C')
    chiffer11 = [9, 2, 2, 0, 1, 1, 2, 0, 5, 5, 6, 2, 7, 7, 7, 4, 9, 5]
    chiffer12 = [5, 0, 4, 1, 4, 9, 8, 6, 5, 5, 7, 8, 0, 5, 6, 1, 4, 0]
    chiffer13 = [0, 4, 3, 4, 4, 3, 4, 3, 2, 3, 5, 7, 9, 2, 5, 9, 9, 1, 6, 5, 7, 3, 4, 6, 2, 2, 6, 9, 9]
    chiffer14 = [3, 0, 8, 5, 9, 2, 3, 9, 9, 9, 9, 3, 7, 4, 0, 5, 3, 8, 7, 2, 3, 6, 5, 5, 5, 5, 8, 2, 2]
    chiffer15 = [25, 0, 11, 2, 16, 24, 13, 15, 19, 10, 9, 11, 17, 11, 7, 11, 20, 3, 8]
    
    def test_FF3_128_Sample1(self): #Sample #1
        cipher = FF3(self.key1, 10)
        self.assertEqual(cipher.encrypt(self.clear1, self.tweak1), self.chiffer1)
        self.assertEqual(cipher.decrypt(self.chiffer1, self.tweak1), self.clear1)
        
    def test_FF3_128_Sample2(self): #Sample #2
        cipher = FF3(self.key1, 10)
        self.assertEqual(cipher.encrypt(self.clear1, self.tweak2), self.chiffer2)
        self.assertEqual(cipher.decrypt(self.chiffer2, self.tweak2), self.clear1)
        
    def test_FF3_128_Sample3(self): #Sample #3
        cipher = FF3(self.key1, 10)
        self.assertEqual(cipher.encrypt(self.clear3, self.tweak1), self.chiffer3)
        self.assertEqual(cipher.decrypt(self.chiffer3, self.tweak1), self.clear3)
     
    def test_FF3_128_Sample4(self): #Sample #4
        cipher = FF3(self.key1, 10)
        self.assertEqual(cipher.encrypt(self.clear3, self.tweak4), self.chiffer4)
        self.assertEqual(cipher.decrypt(self.chiffer4, self.tweak4), self.clear3)      
        
    def test_FF1_128_Sample5(self): #Sample #5
        cipher = FF3(self.key1, 26)
        self.assertEqual(cipher.encrypt(self.clear5, self.tweak2), self.chiffer5)
        self.assertEqual(cipher.decrypt(self.chiffer5, self.tweak2), self.clear5)
          
    def test_FF1_192_Sample6(self): #Sample #6
        cipher = FF3(self.key6, 10)
        self.assertEqual(cipher.encrypt(self.clear1, self.tweak1), self.chiffer6)
        self.assertEqual(cipher.decrypt(self.chiffer6, self.tweak1), self.clear1)

    def test_FF1_192_Sample7(self): #Sample #7
        cipher = FF3(self.key6, 10)
        self.assertEqual(cipher.encrypt(self.clear1, self.tweak2), self.chiffer7)
        self.assertEqual(cipher.decrypt(self.chiffer7, self.tweak2), self.clear1)      
       
    def test_FF1_192_Sample8(self): #Sample #8
        cipher = FF3(self.key6, 10)
        self.assertEqual(cipher.encrypt(self.clear3, self.tweak1), self.chiffer8)
        self.assertEqual(cipher.decrypt(self.chiffer8, self.tweak1), self.clear3)
         
    def test_FF3_192_Sample9(self): #Sample #9
        cipher = FF3(self.key6, 10)
        self.assertEqual(cipher.encrypt(self.clear3, self.tweak4), self.chiffer9)
        self.assertEqual(cipher.decrypt(self.chiffer9, self.tweak4), self.clear3)   
        
    def test_FF3_192_Sample10(self): #Sample #10
        cipher = FF3(self.key6, 26)
        self.assertEqual(cipher.encrypt(self.clear5, self.tweak2), self.chiffer10)
        self.assertEqual(cipher.decrypt(self.chiffer10, self.tweak2), self.clear5)   
          
    def test_FF1_256_Sample11(self): #Sample #11
        cipher = FF3(self.key11, 10)
        self.assertEqual(cipher.encrypt(self.clear1, self.tweak1), self.chiffer11)
        self.assertEqual(cipher.decrypt(self.chiffer11, self.tweak1), self.clear1)

    def test_FF1_256_Sample12(self): #Sample #12
        cipher = FF3(self.key11, 10)
        self.assertEqual(cipher.encrypt(self.clear1, self.tweak2), self.chiffer12)
        self.assertEqual(cipher.decrypt(self.chiffer12, self.tweak2), self.clear1)      
       
    def test_FF1_256_Sample13(self): #Sample #13
        cipher = FF3(self.key11, 10)
        self.assertEqual(cipher.encrypt(self.clear3, self.tweak1), self.chiffer13)
        self.assertEqual(cipher.decrypt(self.chiffer13, self.tweak1), self.clear3)
         
    def test_FF3_256_Sample14(self): #Sample #14
        cipher = FF3(self.key11, 10)
        self.assertEqual(cipher.encrypt(self.clear3, self.tweak4), self.chiffer14)
        self.assertEqual(cipher.decrypt(self.chiffer14, self.tweak4), self.clear3)   
        
    def test_FF3_256_Sample15(self): #Sample #15
        cipher = FF3(self.key11, 26)
        self.assertEqual(cipher.encrypt(self.clear5, self.tweak2), self.chiffer15)
        self.assertEqual(cipher.decrypt(self.chiffer15, self.tweak2), self.clear5) 