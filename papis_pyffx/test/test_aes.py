import unittest
from Crypto.Cipher import AES

class AESTest(unittest.TestCase):
    def test_AES_ECB_128(self):
        #Examples from ADVANCED ENCRYPTION STANDARD (AES)
        #https://csrc.nist.gov/csrc/media/publications/fips/197/final/documents/fips-197.pdf
        #page 35/36
        key = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
        plaintext = bytes.fromhex('00112233445566778899aabbccddeeff')
        chiffertext = bytes.fromhex('69c4e0d86a7b0430d8cdb78070b4c55a')
        
        cipher = AES.new(key, AES.MODE_ECB)
        self.assertEqual(cipher.encrypt(plaintext), chiffertext)
        self.assertEqual(cipher.decrypt(chiffertext), plaintext)
    
    def test_AES_ECB_192(self):
        #page 38/39
        key = bytes.fromhex('000102030405060708090a0b0c0d0e0f1011121314151617')
        plaintext = bytes.fromhex('00112233445566778899aabbccddeeff')
        chiffertext = bytes.fromhex('dda97ca4864cdfe06eaf70a0ec0d7191')
        
        cipher = AES.new(key, AES.MODE_ECB)
        self.assertEqual(cipher.encrypt(plaintext), chiffertext)
        self.assertEqual(cipher.decrypt(chiffertext), plaintext)
        
    def test_AES_ECB_256(self):
        #page 42/43
        key = bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f')
        plaintext = bytes.fromhex('00112233445566778899aabbccddeeff')
        chiffertext = bytes.fromhex('8ea2b7ca516745bfeafc49904b496089')
        
        cipher = AES.new(key, AES.MODE_ECB)
        self.assertEqual(cipher.encrypt(plaintext), chiffertext)
        self.assertEqual(cipher.decrypt(chiffertext), plaintext)
        
    def test_AES_CBC(self):
        key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
        iv = bytes.fromhex('00010203 04050607 08090A0B 0C0D0E0F')
        plaintext = bytes.fromhex('6BC1BEE2 2E409F96 E93D7E11 7393172A AE2D8A57 1E03AC9C 9EB76FAC 45AF8E51 30C81C46 A35CE411 E5FBC119 1A0A52EF F69F2445 DF4F9B17 AD2B417B E66C3710')
        chiffertext = bytes.fromhex('7649ABAC 8119B246 CEE98E9B 12E9197D 5086CB9B 507219EE 95DB113A 917678B2 73BED6B8 E3C1743B 7116E69E 22229516 3FF1CAA1 681FAC09 120ECA30 7586E1A7')

        cipher = AES.new(key, AES.MODE_CBC, iv =iv)
        self.assertEqual(cipher.encrypt(plaintext), chiffertext)
        cipher = AES.new(key, AES.MODE_CBC, iv =iv)
        self.assertEqual(cipher.decrypt(chiffertext), plaintext)
    
        
        