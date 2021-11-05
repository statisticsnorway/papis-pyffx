import unittest
import tempfile
from ..load_key import load_key_from_file

class TestLoadKey(unittest.TestCase):
    keyCvc = (('2b7e151628aed2a6abf7158809cf4f3c' , '7df76b0c1ab899b33e42f047b91b546f'),
    ('2b7e151628aed2a6abf7158809cf4f3cef4359d8d580aa4f', '9bb8b368857b6adcca96c42a75798efd'),
    ('2b7e151628aed2a6abf7158809cf4f3cef4359d8d580aa4f7f036d6f04fc6a94', '9601b5247154e8ec4019edb6eb8e0f83')
    )
    
    @classmethod
    def setUpClass(cls):
        cls.tmpDir = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.tmpDir.cleanup()
    
    @classmethod
    def helperWriteFile(cls, writeList):
        tmp = tempfile.NamedTemporaryFile('r+', dir=cls.tmpDir.name, delete=False)
        tmp.writelines(writeList)
        tmp.close()
        return tmp.name
    
    def test_Loadkey(self):
        for key, cvc in self.keyCvc:
            tmpName = self.helperWriteFile([key, '\n', cvc, '\n'])
            hexKey = load_key_from_file(tmpName)
            print(hexKey.hex())
            self.assertEqual(hexKey.hex(), key)
            
    def test_WrongKey(self):
        tmpName = self.helperWriteFile([self.keyCvc[0][0], '\n', self.keyCvc[0][0], '\n'])
        with self.assertRaises(ValueError) as cm:
            load_key_from_file(tmpName)
        exception = cm.exception
        self.assertEqual(exception.args[0], 'CVC does not match')
        