import unittest
from unittest.mock import patch
from requests import Response, HTTPError
from dataclasses import dataclass, field
from papis_pyffx.client.client_fpe import ClientFPE

@dataclass
class MockResponse:
    status_code : int = field(default = 200)
    text : str = field(default='')
    json : dict[str, str] = field(default_factory=dict)


class TestClientFpe(unittest.TestCase):
    def setUp(self):
        self.client = ClientFPE('localhost', 8080)
        self.url = 'http://localhost:8080'
    
    @patch('requests.get')
    def test_response_ok(self, mock_get):
        mock_get.return_value = Response()
        mock_get.return_value.status_code = 200
        #Controls that no error is raised
        encrypted_value = self.client.encrypt('12345')

    @patch('requests.get')
    def test_response_nok(self, mock_get):
        mock_get.return_value = Response()
        mock_get.return_value.status_code = 404
        with self.assertRaises(HTTPError) as exc:
            encrypted_value = self.client.encrypt('12345')
        self.assertEqual(str(exc.exception), '404 Client Error: None for url: None')

    @patch('requests.get')
    def test_encrypt(self, mock_get):
        mock_get.return_value = MockResponse(text='encrypted_value')

        encrypted_value = self.client.encrypt('12345')
        self.assertEqual(encrypted_value, 'encrypted_value')
        mock_get.assert_called_once_with(f'{self.url}/encrypt/12345')
        
    @patch('requests.get')
    def test_decrypt(self, mock_get):
        mock_get.return_value = MockResponse(text='decrypted_value')

        decrypted_value = self.client.decrypt('encrypted_value')
        self.assertEqual(decrypted_value, 'decrypted_value')
        mock_get.assert_called_once_with(f'{self.url}/decrypt/encrypted_value')

    @patch('requests.post')
    def test_encrypt_set(self, mock_post):
        mock_response_json = lambda: {'value1': 'encrypted1', 'value2': 'encrypted2'}
        mock_post.return_value = MockResponse(json = mock_response_json)

        encrypted_values = self.client.encrypt_set(['123', '456'])

        self.assertEqual(encrypted_values, {'value1': 'encrypted1', 'value2': 'encrypted2'})
        mock_post.assert_called_once_with(f'{self.url}/encrypt_set/', json=['123', '456'])

    @patch('requests.post')
    def test_decrypt_set(self, mock_post):
        mock_response_json = lambda: {'value1': 'decrypted1', 'value2': 'decrypted2'}
        mock_post.return_value = MockResponse(json = mock_response_json)

        decrypted_values = self.client.decrypt_set(['encrypted1', 'encrypted2'])

        self.assertEqual(decrypted_values, {'value1': 'decrypted1', 'value2': 'decrypted2'})
        mock_post.assert_called_once_with(f'{self.url}/decrypt_set/', json=['encrypted1', 'encrypted2'])

    @patch('requests.get')
    def test_max_query_size(self, mock_get):
        mock_get.return_value = MockResponse(text='100')

        max_size = self.client.max_query_size()

        self.assertEqual(max_size, 100)
        mock_get.assert_called_once_with(f'{self.url}/max_query_size')

    @patch('requests.get')
    def test_get_alphabet(self, mock_get):
        mock_get.return_value = MockResponse(text='abcdefghijklmnopqrstuvwxyz')

        alphabet = self.client.get_alphabet()

        self.assertEqual(alphabet, 'abcdefghijklmnopqrstuvwxyz')
        mock_get.assert_called_once_with(f'{self.url}/get_alphabet')
