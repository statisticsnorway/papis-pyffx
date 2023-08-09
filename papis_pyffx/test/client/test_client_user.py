import unittest
from unittest.mock import Mock, patch
from requests import Response, HTTPError
from dataclasses import dataclass, field
from papis_pyffx.protocol.workObject import WorkObject, FileTypes
from papis_pyffx.client.client_user import ClientUser
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

test_public_key = '-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAymySVbX8SkSQTLTTY8/N\nGYLVBa2qzZPMVkr92y5oVQOVu5MQS/8NX8v3dlkRkbumLqUZuYaxLhFuf1crYBJP\nQyAhxRB+ljB3ZgxL9qf6DfjIE+yUi+5u4zmoipCBH7agdfcFUsrDDJa0/xkjz5Hr\nMGW/hYq1iJFAgI9qYTe8zDBv5/jF8ROzQmkcY6pnDS5XCvxi1ZKzwYFOEti4tZUW\n4QZ0chDf9Rdyv043hXgN94KEbLOgw9FSXZ6siP37Ft48B+naA3fDRznrNwHMP+XO\n2JNHWUxRGnprsXNpxDnmXUFwoURnYeqGTLZiu8L6Y3bpZjvbA+lEGwzIky8a1GaN\nRPEb6wuZDiw3mr32sy0gc/n0XFYPFF9AZu8X/WvvW97HsgUfrTI1AK3iQ9/iB0gq\n+b1WeHC/8a8ba04zzNLWf5aP/Bqp3c4YOCHaZqNBk05vxkwkG2N1ZykC2u7Zkksu\nrTlxcTfPufBeEFCw9k2XGO3WPO+yWB6eEGofKdgHIzXBGcJscmVE+h7blLLh4ghk\nYIkaPrio31gN3EUCb6ttQPsVBrn1/gtG5w9rEghEO93iQJvky6x5ZYEwPIQgkD4a\nHgRhG5yB14mfQ3Ip0vyD/kCHSziUF5Jd3Ark+DMjixasVYAizY3iKTBYzAt7+OVK\n6JYeGpNm4MppVfpVIHDL9mMCAwEAAQ==\n-----END PUBLIC KEY-----'
test_user_dict = {'user_name': 'test_user', 'password': 'Ken sent me', 'encrypted': False}

@dataclass
class MockResponse:
    status_code : int = field(default = 200)
    text : str = field(default='')
    json : dict[str, str] = field(default_factory=dict)

class TestClientUser(unittest.TestCase):
    def setUp(self):
        self.client = ClientUser('localhost', 8080, False)
        self.url = 'http://localhost:8080'

    def test_init(self):
        host, port = 'localhost', 8080
        client_http = ClientUser(host, port, False)
        self.assertIsInstance(client_http.base_url, str)
        self.assertEqual(client_http.base_url, f"http://{host}:{port}")

        client_https = ClientUser(host, port, True)
        self.assertIsInstance(client_https.base_url, str)
        self.assertEqual(client_https.base_url, f"https://{host}:{port}")


    @patch('requests.post')
    def test_login_user_no_encrypt(self, mock_post):
        mock_post.return_value = MockResponse(text=test_user_dict['user_name'])
        result = self.client.login_user(test_user_dict['user_name'], test_user_dict['password'], False)

        self.assertEqual(result, test_user_dict['user_name'])
        mock_post.assert_called_once_with(f'{self.url}/login_user', json=test_user_dict)

    @patch('requests.post')
    @patch('requests.get')
    def test_login_user_encrypt(self, mock_get, mock_post):
        mock_get.return_value = MockResponse(text = test_public_key)
        mock_post.return_value = MockResponse(text=test_user_dict['user_name'])
        result = self.client.login_user(test_user_dict['user_name'], test_user_dict['password'], True)

        self.assertEqual(result, test_user_dict['user_name'])
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args_list[0][0][0], f'{self.url}/login_user')
        js = mock_post.call_args_list[0][1]['json']
        test_dict = test_user_dict.copy()
        test_dict['encrypted'] = True
        test_dict['password'] = js['password']
        self.assertEqual(js, test_dict)

    @patch('requests.get')
    def test_logout_user(self, mock_get):
        user_name = "test_user"
        mock_get.return_value = MockResponse(text = user_name)
        result = self.client.logout_user(user_name)

        self.assertEqual(result, user_name)
        mock_get.assert_called_once_with(f'{self.url}/logout/{user_name}')

    @patch('requests.get')
    def test_keep_alive(self, mock_get):
        user_name = "test_user"
        mock_get.return_value = MockResponse(text = user_name)
        result = self.client.keep_alive(user_name)
        
        self.assertEqual(result, user_name)
        mock_get.assert_called_once_with(f'{self.url}/keep_alive/{user_name}')


    @patch('requests.get')
    def test_get_public_key(self, mock_get):
        user_name = "test_user"
        mock_get.return_value = MockResponse(text = test_public_key)
        result = self.client.get_public_key()
        
        self.assertEqual(result, test_public_key)
        mock_get.assert_called_once_with(f'{self.url}/get_public_key/')


    @patch('requests.get')
    def test_get_hash_salt(self, mock_get):
        mock_get.return_value = MockResponse(text = "mock_hash_salt")
        result = self.client.get_hash_salt()
        
        self.assertEqual(result, "mock_hash_salt")
        mock_get.assert_called_once_with(f'{self.url}/get_hash_salt/')

