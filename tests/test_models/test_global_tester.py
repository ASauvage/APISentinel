import unittest
from unittest.mock import patch, mock_open
from models.global_tester import GlobalTester


class MockedService:
    path = 'test_path'
    options = {'request_delay': 100}
    headers = {'key': 'value'}

    def __init__(self, name: str):
        self.name = name

    def url(self, env, api):
        return 'http://example.com'


class TestGlobalTester(unittest.TestCase):
    @patch('models.global_tester.apitester', return_value=(None, list()))
    @patch('models.global_tester.Service', side_effect=MockedService)
    @patch('models.global_tester.os.listdir', return_value=['test_api.json'])
    @patch('models.global_tester.os.path.isfile', return_value=True)
    @patch('models.global_tester.open', new=mock_open(read_data='extended_paths:\n- /extra\nquery_specs:\n  headers:\n    test: 123\n  params:\n    test: 1\n'))
    @patch('models.global_tester.MongoCon')
    def test_test_executer_success(self, mockpatch_apitester, mockpatch_service, mockpatch_listdir, mockpatch_isfile, mockpatch_save_results):
        tester = GlobalTester('production', 'TestService')
        print(tester.tests[0])
        assert len(tester.tests) == 1
        assert tester.tests[0]['test_info']['title'] == 'Test on /test_api/extra'
        assert tester.tests[0]['service'] == 'TestService'
        assert tester.tests[0]['env'] == 'production'
        assert tester.tests[0]['request'] == 'http://example.com/extra'
        print(tester.tests[0]['headers'])
        assert tester.tests[0]['headers'] == {'User-Agent': 'test-mapping', 'referer': 'test-mapping', 'key': 'value', 'test': 123}
        assert tester.tests[0]['params'] == {'test': 1}
        assert tester.tests[0]['status']
        assert len(tester.tests[0]['errors']) == 0
        assert tester.tests[0]['api_response'] is None
        mockpatch_save_results.assert_called_once()

    @patch('models.global_tester.apitester', return_value=(None, ['fake_error_object']))
    @patch('models.global_tester.Service', side_effect=MockedService)
    @patch('models.global_tester.os.listdir', return_value=['test_api.json'])
    @patch('models.global_tester.os.path.isfile', return_value=True)
    @patch('models.global_tester.open', new=mock_open(read_data="extended_paths:\n- /extra\n"))
    @patch('models.global_tester.MongoCon')
    def test_test_executer_failure(self, mockpatch_apitester, mockpatch_service, mockpatch_listdir, mockpatch_isfile, mockpatch_save_results):
        tester = GlobalTester('production', 'TestService')
        assert len(tester.tests) == 1
        assert tester.tests[0]['test_info']['title'] == 'Test on /test_api/extra'
        assert tester.tests[0]['service'] == 'TestService'
        assert tester.tests[0]['env'] == 'production'
        assert tester.tests[0]['request'] == 'http://example.com/extra'
        assert tester.tests[0]['headers'] == {'User-Agent': 'test-mapping', 'referer': 'test-mapping', 'key': 'value'}
        assert tester.tests[0]['params'] == {}
        assert not tester.tests[0]['status']
        assert len(tester.tests[0]['errors']) == 1
        assert tester.tests[0]['api_response'] is None
        mockpatch_save_results.assert_called_once()


if __name__ == '__main__':
    unittest.main()
