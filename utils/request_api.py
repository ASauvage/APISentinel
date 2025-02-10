from requests import get, JSONDecodeError

HEADERS = {
    "User-Agent": "test-mapping",
    "referer": 'test-mapping'
}


def api_get_json(*args, **kwargs):
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"].update(HEADERS)

    response = get(*args, **kwargs)
    try:
        return response.json()
    except JSONDecodeError as e:
        raise e
