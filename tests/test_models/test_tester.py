import unittest
from unittest.mock import patch, MagicMock
from models.service import Service
from models.tester import apitester


class TestTester(unittest.TestCase):
    @patch.multiple('models.tester',
                    api_get_json=MagicMock(return_value=dict(metadata=dict(request_id=1234))),
                    is_mapping_ok=MagicMock(return_value=['error']))
    def test_tester(self):
        result = apitester('production', Service('pokeapi'), '', api='test', query_specs=dict(), filename="item.json")
        assert len(result) == 1
        assert result[0] == 'error'


if __name__ == '__main__':
    unittest.main()
