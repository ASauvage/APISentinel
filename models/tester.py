import os
from models.service import Service
from utils.request_api import api_get_json
from utils.mapping import is_mapping_ok


def apitester(env: str, service: Service, extended_path: str, **specifications):
    response = api_get_json(
        service.url(env, specifications['api']) + extended_path,
        headers=specifications['headers'],
        **specifications['query_specs']
    )

    errors = is_mapping_ok(response, '{}/data/mapping/{}'.format(os.getcwd(), service.path + specifications['filename']))

    return errors
