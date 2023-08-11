import unittest
from unittest.mock import Mock, patch
from dataclasses import dataclass, field
from time import sleep
from papis_pyffx.protocol.workObject import WorkObject, FileTypes
from papis_pyffx.client.client_pseudo_file import ClientPseudoFile, QUEUE_NAMES
from papis_pyffx.helper.reapeated_timer import RepeatedTimer

@dataclass
class MockResponse:
    status_code : int = field(default = 200)
    text : str = field(default='')
    json : dict[str, str] = field(default_factory=dict)

class TestClientPseudoFile(unittest.TestCase):
    def setUp(self):
        self.client = ClientPseudoFile('localhost', 8080, ssh = False, startTimer=False)
        self.url = 'http://localhost:8080'
        self.mock_wo = WorkObject("input.txt", "output.txt", ("fnr", "navn"), FileTypes.MOCK, file_len=10, progress='progress')
        self.di_norm = {name : [self.mock_wo, self.mock_wo] for name in QUEUE_NAMES.values()}
        self.di_json = lambda: {name : [self.mock_wo.asdict(),self.mock_wo.asdict()] for name in QUEUE_NAMES.values()}
    
    def test_init(self):
        host, port = 'localhost', 8080
        client_http = ClientPseudoFile(host, port, ssh = False, startTimer=False)
        self.assertIsInstance(client_http.base_url, str)
        self.assertEqual(client_http.base_url, f"http://{host}:{port}")

        client_https = ClientPseudoFile(host, port, ssh = True, startTimer=False)
        self.assertIsInstance(client_https.base_url, str)
        self.assertEqual(client_https.base_url, f"https://{host}:{port}")

    def test_repeat_timer(self):
        host, port = 'localhost', 8080
        client_http = ClientPseudoFile(host, port, hookTimer=0.1, startTimer=True)
        self.assertEqual(type(client_http._repeatTimer), RepeatedTimer)
        client_http.close()

    @patch('requests.get')
    def test_get_queues(self, mock_get):
        mock_get.return_value = MockResponse(json=self.di_json)
        result = self.client.get_queues()

        self.assertEqual(self.di_norm, result)
        mock_get.assert_called_once_with(f'{self.url}/get_queues')

    @patch('requests.post')
    def test_add(self, mock_post):
        mock_post.return_value = MockResponse(text=self.mock_wo.inn_file_name)
        result = self.client.add("input.txt", "output.txt", ("fnr", "navn"), FileTypes.MOCK, file_len=10, progress='progress', timing = self.mock_wo.timing)

        self.assertEqual(result, "input.txt")
        mock_post.assert_called_once_with(f'{self.url}/add_work', json=self.mock_wo.asdict())

    @patch('requests.post')
    def test_add_work(self, mock_post):
        mock_post.return_value = MockResponse(text=self.mock_wo.inn_file_name)
        result = self.client.add_work(self.mock_wo)

        self.assertEqual(result, self.mock_wo.inn_file_name)
        mock_post.assert_called_once_with(f'{self.url}/add_work', json=self.mock_wo.asdict())

    @patch('requests.post')
    def test_remove_work(self, mock_post):
        mock_post.return_value = MockResponse(text=self.mock_wo.inn_file_name)
        result = self.client.remove_work(self.mock_wo)

        self.assertEqual(result, self.mock_wo.inn_file_name)
        mock_post.assert_called_once_with(f'{self.url}/remove_work', json=self.mock_wo.asdict())



    @patch('requests.get')
    def test_register_after_active_hook(self, mock_get_queues) -> None:
        counter = 0
        def after_active_hook_function(origin : str, to : str, work : WorkObject):
            nonlocal counter
            self.assertEqual(origin, QUEUE_NAMES.ACTIVE.value)
            self.assertTrue(to in (QUEUE_NAMES.DONE.value, QUEUE_NAMES.ERROR.value))
            self.assertTrue(work == self.mock_wo)
            counter += 1

        js_old = {name : list() for name in QUEUE_NAMES.values()} 
        js_new = js_old.copy()  
        js_new[QUEUE_NAMES.DONE.value] = [self.mock_wo.asdict()]
        js_new[QUEUE_NAMES.ERROR.value] = [self.mock_wo.asdict()]
        mock_get_queues.side_effect = [MockResponse(json=lambda : js_old), MockResponse(json=lambda : js_new)]

        self.client.register_after_active_hook(after_active_hook_function)
        self.client._repeatTimerFunction()
        self.assertEqual(counter, 0)
        self.client._repeatTimerFunction()
        self.assertEqual(counter, 2)