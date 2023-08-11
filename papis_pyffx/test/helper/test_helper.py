import string
import unittest
from papis_pyffx.helper.filter import Filter

class TestFiler(unittest.TestCase):
    def setUp(self):
        self.filter = Filter()

    def testFilter(self):
        self.assertEqual(self.filter.filter('Åge Ålsen'), 'gelsen')

    def testUnfilter(self):
        self.assertEqual(self.filter.unfilter('Åge Ålsen', 'egabcd'), 'Åeg Åabcd')

        with self.assertRaises(AttributeError):
            self.filter.unfilter('Åge Ålsen', 'egabcdx')
        
        with self.assertRaises(RuntimeError):
            self.filter.unfilter('Åge Ålsen', 'egab')