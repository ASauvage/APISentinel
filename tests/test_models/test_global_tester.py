import unittest
from unittest.mock import patch, MagicMock
from models.global_tester import GlobalTester


class MockedService:
    path = 'test_path'
    options = {'request_delay': 100}
    headers = {"key": "value"}

    def __init__(self, name: str):
        self.name = name

    def url(self, env, api):
        return "http://example.com"


class TestGlobalTester(unittest.TestCase):
    @patch('models.global_tester.apitester', return_value=list())
    @patch('models.global_tester.Service', side_effect=MockedService)
    @patch('os.listdir', return_value=['test_api.json'])
    @patch('yaml.load', return_value=dict(extended_paths=['/extra']))
    @patch('utils.mongodb.MongoCon.save_results')
    def test_test_executer_success(self, mockpatch_apitester, mockpatch_service, mockpatch_listdir, mockpatch_load, mockpatch_save_results):
        tester = GlobalTester("production", "TestService")
        assert len(tester.tests) == 1
        assert tester.tests[0]['status']
        mockpatch_save_results.assert_called_once()

    @patch('models.global_tester.apitester', return_value=['fake_error_object'])
    @patch('models.global_tester.Service', side_effect=MockedService)
    @patch('os.listdir', return_value=['test_api.json'])
    @patch('yaml.load', return_value=dict(extended_paths=['/extra']))
    @patch('utils.mongodb.MongoCon.save_results')
    def test_test_executer_failure(self, mockpatch_apitester, mockpatch_service, mockpatch_listdir, mockpatch_load, mockpatch_save_results):
        tester = GlobalTester("production", "TestService")
        assert len(tester.tests) == 1
        assert not tester.tests[0]['status']
        assert len(tester.tests[0]['errors']) == 1
        mockpatch_save_results.assert_called_once()


if __name__ == '__main__':
    unittest.main()
