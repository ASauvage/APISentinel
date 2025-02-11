import os
from requests import JSONDecodeError
from models.service import Service
from models.errors import HttpCodeError, NotJsonError
from utils.request_api import api_get_json
from utils.mapping import is_mapping_ok


def apitester(env: str, service: Service, extended_path: str, **specifications) -> tuple[str, list]:
    response = api_get_json(
        service.url(env, specifications['api']) + extended_path,
        **specifications['query_specs']
    )

    resp_to_save = response.text if specifications['save_response'] else None

    if response.status_code in specifications['valid_http_code']:
        try:
            errors = is_mapping_ok(response.json(), '{}/data/mapping/{}'.format(os.getcwd(), service.path + specifications['filename']))
        except JSONDecodeError:
            errors = [NotJsonError()]
    else:
        errors = [HttpCodeError(response.status_code)]

    return resp_to_save, errors
