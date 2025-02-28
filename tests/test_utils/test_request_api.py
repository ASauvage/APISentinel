import unittest
from unittest.mock import patch
from utils.request_api import api_get_json


def mocked_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code):
            self.json_data = dict(args=args, kwargs=kwargs)
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://127.0.0.1/api':
        return MockResponse(200)

    return MockResponse(404)


class TestRequestApi(unittest.TestCase):
    @patch('utils.request_api.get', side_effect=mocked_get)
    def test_api_get_json_no_additional_headers(self, mockpatch):
        response = api_get_json('http://127.0.0.1/api')
        assert response.json() == dict(
            args=('http://127.0.0.1/api',),
            kwargs={'headers': {'Content-Type': 'application/json', 'User-Agent': 'test-mapping', 'referer': 'test-mapping'}}
        )

    @patch('utils.request_api.get', side_effect=mocked_get)
    def test_api_get_json_additional_headers(self, mockpatch):
        response = api_get_json('http://127.0.0.1/api', headers=dict(useragent='test', contenttype="*/*"))
        assert response.json() == dict(
            args=('http://127.0.0.1/api',),
            kwargs={'headers': {'useragent': 'test', 'contenttype': '*/*', 'Content-Type': 'application/json', 'User-Agent': 'test-mapping', 'referer': 'test-mapping'}}
        )


if __name__ == '__main__':
    unittest.main()
