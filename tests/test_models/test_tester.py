import unittest
from unittest.mock import patch, MagicMock
from models.service import Service
from models.tester import apitester


class TestTester(unittest.TestCase):
    @patch.multiple('models.tester',
                    api_get_json=MagicMock(return_value=dict(metadata=dict(request_id=1234))),
                    is_mapping_ok=MagicMock(return_value=['error']))
    def test_tester_save_response_false(self):
        response, result = apitester('production', Service('pokeapi'), '', api='test', query_specs=dict(), save_response=False, filename="item.json")
        assert response is None
        assert len(result) == 1
        assert result[0] == 'error'

    @patch.multiple('models.tester',
                    api_get_json=MagicMock(return_value=dict(metadata=dict(request_id=1234))),
                    is_mapping_ok=MagicMock(return_value=['error']))
    def test_tester_save_response_true(self):
        response, result = apitester('production', Service('pokeapi'), '', api='test', query_specs=dict(), save_response=True, filename="item.json")
        assert response == '{"metadata": {"request_id": 1234}}'
        assert len(result) == 1
        assert result[0] == 'error'


if __name__ == '__main__':
    unittest.main()
