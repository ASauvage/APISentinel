from requests import get, Response

HEADERS = {
    "User-Agent": "test-mapping",
    "referer": 'test-mapping'
}


def api_get_json(*args, **kwargs) -> Response:
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"].update(HEADERS)

    return get(*args, **kwargs)
