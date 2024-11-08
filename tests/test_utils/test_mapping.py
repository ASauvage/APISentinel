import unittest
from copy import deepcopy
from models.errors import *
from utils.mapping import is_mapping_ok


DATA = [
    {
        "metadata": {
            "request_id": 1234,
            # "optional_field": False,
            "nullable_field": None,
            "datetime": "2024-11-08T09:20:10Z"
        },
        "data": [
            "hello",
            "please",
            "helpme"
        ],
        "enums": "asauvage"
    }
]


class TestMapping(unittest.TestCase):
    def test_is_mapping_ok_no_error(self):
        errors = is_mapping_ok(DATA, 'tests/test_utils/test_mapping.json')
        assert len(errors) == 0

    def test_is_mapping_ok_missing_field_error(self):
        alt_data = deepcopy(DATA)
        del alt_data[0]['metadata']['request_id']

        errors = is_mapping_ok(alt_data, 'tests/test_utils/test_mapping.json')
        assert len(errors) == 1
        assert isinstance(errors[0], MissingFieldError)
        assert errors[0].as_dict() == dict(explicit_content="MissingFieldError", field=[0, 'metadata', 'request_id'])
        assert errors[0].__str__() == "MissingFieldError: field '[0, 'metadata', 'request_id']' is missing"

    def test_is_mapping_ok_wrong_type_error(self):
        alt_data = deepcopy(DATA)
        alt_data[0]['metadata']['request_id'] = '1234'

        errors = is_mapping_ok(alt_data, 'tests/test_utils/test_mapping.json')
        assert len(errors) == 1
        assert isinstance(errors[0], WrongTypeError)
        assert errors[0].as_dict() == dict(explicit_content="WrongTypeError", field=[0, 'metadata', 'request_id'],
                                           expected=[int, float], received=str)
        assert errors[0].__str__() == "WrongTypeError: '[0, 'metadata', 'request_id']' should be a(n) [<class 'int'>, <class 'float'>] not <class 'str'>"

    def test_is_mapping_ok_wrong_value_error(self):
        alt_data = deepcopy(DATA)
        alt_data[0]['enums'] = 'sauvagea'

        errors = is_mapping_ok(alt_data, 'tests/test_utils/test_mapping.json')
        assert len(errors) == 1
        assert isinstance(errors[0], WrongValueError)
        assert errors[0].as_dict() == dict(explicit_content="WrongValueError", field=[0, 'enums'],
                                           expected=['on', 'off', 'asauvage'], received='sauvagea')
        assert errors[0].__str__() == "WrongValueError: '[0, 'enums']' should be in ['on', 'off', 'asauvage'] but got 'sauvagea' instead"

    def test_is_mapping_ok_wrong_format_error(self):
        alt_data = deepcopy(DATA)
        alt_data[0]['metadata']['request_id'] = 12.2

        errors = is_mapping_ok(alt_data, 'tests/test_utils/test_mapping.json')
        assert len(errors) == 1
        assert isinstance(errors[0], WrongFormatError)
        assert errors[0].as_dict() == dict(explicit_content="WrongFormatError", field=[0, 'metadata', 'request_id'],
                                           expected='int', received=float)
        assert errors[0].__str__() == "WrongFormatError: '[0, 'metadata', 'request_id']' should be a(n) int but got '<class 'float'>' instead"

    def test_is_mapping_ok_wrong_datetime_format_error(self):
        alt_data = deepcopy(DATA)
        alt_data[0]['metadata']['datetime'] = 'not a datetime'

        errors = is_mapping_ok(alt_data, 'tests/test_utils/test_mapping.json')
        assert len(errors) == 1
        assert isinstance(errors[0], WrongDatetimeFormatError)
        assert errors[0].as_dict() == dict(explicit_content="WrongFormatError", field=[0, 'metadata', 'datetime'],
                                           format='datetime', received='not a datetime')
        assert errors[0].__str__() == "WrongFormatError: '[0, 'metadata', 'datetime']' not in datetime format, got 'not a datetime'"

    def test_is_mapping_ok_regex_error(self):
        alt_data = deepcopy(DATA)
        alt_data[0]['data'][1] = 'pl34s3'

        errors = is_mapping_ok(alt_data, 'tests/test_utils/test_mapping.json')
        assert len(errors) == 1
        assert isinstance(errors[0], RegexError)
        assert errors[0].as_dict() == dict(explicit_content="RegexError", field=[0, 'data', 1],
                                           pattern='^[a-z]*$')
        assert errors[0].__str__() == "RegexError: '[0, 'data', 1]' should match pattern '^[a-z]*$'"

    def test_is_mapping_ok_minlen_error(self):
        alt_data = deepcopy(DATA)
        alt_data[0]['data'] = []

        errors = is_mapping_ok(alt_data, 'tests/test_utils/test_mapping.json')
        assert len(errors) == 1
        assert isinstance(errors[0], MinLenghtError)
        assert errors[0].as_dict() == dict(explicit_content="MinLenghtError", field=[0, 'data'],
                                           expected=1, received=0)
        assert errors[0].__str__() == "MinLenghtError: '[0, 'data']' got 0 values but 1 minimum required"

    def test_is_mapping_ok_maxlen_error(self):
        alt_data = deepcopy(DATA)
        alt_data[0]['data'].append('iamunderthewater')

        errors = is_mapping_ok(alt_data, 'tests/test_utils/test_mapping.json')
        assert len(errors) == 1
        assert isinstance(errors[0], MaxLenghtError)
        assert errors[0].as_dict() == dict(explicit_content="MaxLenghtError", field=[0, 'data'],
                                           expected=3, received=4)
        assert errors[0].__str__() == "MaxLenghtError: '[0, 'data']' got 4 values but 3 maximum required"
