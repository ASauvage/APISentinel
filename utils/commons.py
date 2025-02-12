import json
from uuid import uuid4
from datetime import datetime
from functools import reduce
from copy import deepcopy


def get_value(data: dict, keys: list):
    return reduce(lambda d, key: d[key], keys, data)


def get_mapping_ref(mapping: dict, ref_path: str, ref: str):
    with open(f"{ref_path}/generics/{ref}.json") as json_file:
        return mapping | json.load(json_file)


def query_specs_secret(query_specs: dict) -> tuple[dict, dict]:
    query_specs_hidden = deepcopy(query_specs)

    for spec_name, spec_value in query_specs.items():
        for key, value in spec_value.items():
            try:
                if value.startswith("$secret:"):
                    query_specs[spec_name][key] = value[8:]
                    query_specs_hidden[spec_name][key] = "****************"
            except AttributeError:
                pass

    return query_specs, query_specs_hidden


# 230918-203654-545d6291
def generate_session_id() -> str:
    return "{date}-{uuid}".format(date=datetime.now().strftime('%y%m%d-%H%M%S'),
                                  uuid=str(uuid4())[:8])
