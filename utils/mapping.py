import json
import re
from models.errors import *
from utils.commons import get_value
from datetime import datetime

TYPE = {
    'Object': [dict],
    'Array': [list, tuple],
    'String': [str],
    'Number': [int, float],
    'Boolean': [bool],
    'Null': [type(None)]
}

FORMAT = {
    'int': int,
    'float': float,
    'datetime': datetime
}


def is_mapping_ok(response: dict, mapping_path: str) -> list:
    with open(mapping_path, 'r') as file:
        mapping_json = json.load(file)

        errors = []
        check_field([], mapping_json, response, errors)

        return errors


def check_field(path: list, mapping: dict, response: dict, errors: list) -> list:
    """

    :param path: list of path in response (exemple: ["properties", 0, "name"])
    :param mapping: dict of mapping for the path (exemple: {"id": {"_type": "String"}})
    :param response: API response
    :param errors: errors list
    :return: error list
    """
    for field_name, field_value in mapping.items():
        try:
            # variable declaration
            value_path = path + [field_name] if field_name != "_tmpfield" else path
            value_type = TYPE[field_value['_type']].copy()
            value = get_value(response, value_path)

            # check _nullable
            if '_nullable' in field_value:
                value_type += [type(None)]

            # check _type
            if type(value) not in value_type:
                errors.append(WrongTypeError(value_path, type(value), value_type))
                continue

            # check for type
            if value is not None:
                # check _format
                if '_format' in field_value:
                    if field_value['_format'] == 'datetime':
                        try:
                            datetime.fromisoformat(value)
                        except ValueError:
                            errors.append(WrongDatetimeFormatError(value_path, value))
                    elif not isinstance(value, FORMAT[field_value['_format']]):
                        errors.append(WrongFormatError(value_path, type(value), field_value['_format']))

                # check _enum
                if '_enums' in field_value and value not in field_value['_enums']:
                    errors.append(WrongValueError(value_path, value, field_value['_enums']))

                # check _regex
                if '_regex' in field_value and not re.search(field_value['_regex'], value):
                    errors.append(RegexError(value_path, field_value['_regex']))

                # for each type
                if field_value['_type'] == "Object":
                    check_field(value_path, field_value['_properties'], response, errors)

                if field_value['_type'] == "Array":
                    # check _minlen and _maxlen
                    if '_minlen' in field_value and field_value['_minlen'] > len(value):
                        errors.append(MinLenghtError(value_path, len(value), field_value['_minlen']))
                    if '_maxlen' in field_value and field_value['_maxlen'] < len(value):
                        errors.append(MaxLenghtError(value_path, len(value), field_value['_maxlen']))

                    for index in range(len(get_value(response, value_path))):
                        tmp_errors = list()
                        for map in field_value['_values']:
                            tmp_errors.append(list())
                            check_field(value_path + [index], {'_tmpfield': map}, response, tmp_errors[-1])

                            # FixMe
                            if len(tmp_errors[-1]) == 0:
                                break

                        for error in min(tmp_errors, key=len):
                            errors.append(error)

        except KeyError:
            if '_optional' not in field_value or not field_value['_optional']:
                errors.append(MissingFieldError(path + [field_name]))

    return errors
