import unittest
from utils.commons import get_value, generate_session_id


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
