import json
from uuid import uuid4
from datetime import datetime
from functools import reduce


def get_value(data: dict, keys: list):
    return reduce(lambda d, key: d[key], keys, data)


def get_mapping_ref(mapping: dict, ref_path: str, ref: str):
    with open(f"{ref_path}/generics/{ref}.json") as json_file:
        return mapping | json.load(json_file)


# 230918-203654-545d6291
def generate_session_id() -> str:
    return "{date}-{uuid}".format(date=datetime.now().strftime('%y%m%d-%H%M%S'),
                                  uuid=str(uuid4())[:8])
