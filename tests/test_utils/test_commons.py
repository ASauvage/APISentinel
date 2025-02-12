import unittest
from utils.commons import get_value, generate_session_id, query_specs_secret


class TestCommons(unittest.TestCase):
    def test_get_value(self):
        assert get_value(data={'metadata': {'request_id': '1234', 'tests': [{'id': 1}, {'id': 2}]}},
                         keys=['metadata', 'tests', 1, 'id']) == 2

    def test_generate_session_id(self):
        session_id = generate_session_id()
        assert isinstance(session_id, str)
        assert len(session_id) == 22
        assert session_id[:6].isdigit()
        assert session_id[7:13].isdigit()
        assert session_id != generate_session_id()

    def test_query_specs_secret(self):
        value, hidden_value = query_specs_secret(dict(
            headers={'secret': '$secret:my_secret', 'user': 'asauvage'},
            params={'id': 2, 'secret_id': '$secret:23'}
        ))
        assert value['headers']['secret'] == 'my_secret'
        assert hidden_value['headers']['secret'] == '****************'
        assert hidden_value['headers']['user'] == 'asauvage'
        assert hidden_value['params']['id'] == 2
        assert value['params']['secret_id'] == '23'
        assert hidden_value['params']['secret_id'] == '****************'


if __name__ == '__main__':
    unittest.main()
