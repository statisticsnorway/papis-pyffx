import unittest
from papis_pyffx.helper.crypto_rsa import CryptoRSA

class TestCryptoRSA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.crypto_rsa = CryptoRSA()

    def test_export_public_key(self):
        public_key = self.crypto_rsa.export_public_key()
        self.assertTrue(isinstance(public_key, str))
        self.assertTrue(public_key.startswith('-----BEGIN PUBLIC KEY-----'))
        self.assertTrue(public_key.endswith('-----END PUBLIC KEY-----'))

    def test_encrypt_data(self):
        data = "Ken sent me"
        public_key = self.crypto_rsa.export_public_key()

        encrypted_data = CryptoRSA.encrypt_data(data, public_key)
        self.assertTrue(isinstance(encrypted_data, str))

    def test_decrypt_data(self):
        data = "Ken sent me"
        public_key = self.crypto_rsa.export_public_key()
        encrypted_data = CryptoRSA.encrypt_data(data, public_key)

        decrypted_data = self.crypto_rsa.decrypt_data(encrypted_data)
        self.assertEqual(decrypted_data, data)

    def test_invalid_decryption_error(self):
        # Test decryption with invalid data (e.g., corrupted or wrong key)
        invalid_data = "invalid data"
        with self.assertRaises(ValueError):
            self.crypto_rsa.decrypt_data(invalid_data)

    def test_invalid_decryption_wrong_data(self):
        # Test decryption with invalid data (e.g., corrupted or wrong key)
        invalid_data = "0123456789abcdef" * 64
        decrypted_data = self.crypto_rsa.decrypt_data(invalid_data)
        self.assertIsNone(decrypted_data)

if __name__ == "__main__":
    unittest.main()
