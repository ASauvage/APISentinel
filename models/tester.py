import os
import json
from models.service import Service
from utils.request_api import api_get_json
from utils.mapping import is_mapping_ok


def apitester(env: str, service: Service, extended_path: str, **specifications) -> tuple[str, list]:
    response = api_get_json(
        service.url(env, specifications['api']) + extended_path,
        **specifications['query_specs']
    )

    if specifications['save_response']:
        resp_to_save = json.dumps(response, ensure_ascii=True)
    else:
        resp_to_save = None

    errors = is_mapping_ok(response, '{}/data/mapping/{}'.format(os.getcwd(), service.path + specifications['filename']))

    return resp_to_save, errors
