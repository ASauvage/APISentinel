import unittest
from requests import Response
from unittest.mock import patch, MagicMock
from models.service import Service
from models.tester import apitester


mock_response = Response()
mock_response.status_code = 200
mock_response._content = b'{"metadata": {"request_id": 1234}}'


class TestTester(unittest.TestCase):
    @patch.multiple('models.tester',
                    api_get_json=MagicMock(return_value=mock_response),
                    is_mapping_ok=MagicMock(return_value=['error']))
    def test_tester_save_response_false(self):
        response, result = apitester('production', Service('pokeapi'), '', api='test', query_specs=dict(), filename="item.json",
                                     save_response=False, save_response_on_error=False, valid_http_code=[200])
        assert response is None
        assert len(result) == 1
        assert result[0] == 'error'

    @patch.multiple('models.tester',
                    api_get_json=MagicMock(return_value=mock_response),
                    is_mapping_ok=MagicMock(return_value=['error']))
    def test_tester_save_response_true(self):
        response, result = apitester('production', Service('pokeapi'), '', api='test', query_specs=dict(), filename="item.json",
                                     save_response=True, save_response_on_error=False, valid_http_code=[200])
        assert response == '{"metadata": {"request_id": 1234}}'
        assert len(result) == 1
        assert result[0] == 'error'

    @patch.multiple('models.tester',
                    api_get_json=MagicMock(return_value=mock_response),
                    is_mapping_ok=MagicMock(return_value=[]))
    def test_tester_http_code_error(self):
        response, result = apitester('production', Service('pokeapi'), '', api='test', query_specs=dict(), filename="item.json",
                                     save_response=False, save_response_on_error=False, valid_http_code=[400])
        assert response is None
        assert len(result) == 1
        assert result[0].__str__() == 'HttpCodeError: request return an error code 200'


if __name__ == '__main__':
    unittest.main()
