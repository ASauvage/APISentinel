from uuid import uuid4
from datetime import datetime
from functools import reduce


def get_value(data: dict, keys: list):
    return reduce(lambda d, key: d[key], keys, data)


# 230918-203654-545d6291
def generate_session_id() -> str:
    return "{date}-{uuid}".format(date=datetime.now().strftime('%y%m%d-%H%M%S'),
                                  uuid=str(uuid4())[:8])
