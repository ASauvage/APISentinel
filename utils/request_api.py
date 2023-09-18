from requests import get

HEADERS = {
    "User-Agent": "test-mapping",
    "referer": 'test-mapping'
}


def api_get_json(*args, **kwargs):
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"].update(HEADERS)

    try:
        return get(*args, **kwargs).json()
    except Exception as e:
        raise e
