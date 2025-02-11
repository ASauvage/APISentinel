import unittest
from models.errors import *


class TestErrors(unittest.TestCase):
    def test_error(self):
        error = Error()
        assert error.__str__() == "UnknownError: unexpected error occured"
        assert error.as_dict() == dict(
            explicit_content='UnknownError'
        )

    def test_http_code_error(self):
        error = HttpCodeError(503)
        assert error.__str__() == "HttpCodeError: request return an error code 503"
        assert error.as_dict() == dict(
            explicit_content="HttpCodeError",
            status_code=503
        )

    def test_not_json_error(self):
        error = NotJsonError()
        assert error.__str__() == "NotJsonError: response did not return content in JSON format"
        assert error.as_dict() == dict(
            explicit_content="NotJsonError"
        )

    def test_missing_field_error(self):
        error = MissingFieldError(['field', 0, 'subfield'])
        assert error.__str__() == "MissingFieldError: field 'field.0.subfield' is missing"
        assert error.as_dict() == dict(
            explicit_content='MissingFieldError',
            field=['field', 0, 'subfield']
        )

    def test_wrong_type_error(self):
        error = WrongTypeError(['field', 0, 'subfield'], str, [int, float])
        assert error.__str__() == "WrongTypeError: 'field.0.subfield' should be a(n) ['int', 'float'] not 'str'"
        assert error.as_dict() == dict(
            explicit_content='WrongTypeError',
            field=['field', 0, 'subfield'],
            received=str,
            expected=[int, float]
        )

    def test_wrong_value_error(self):
        error = WrongValueError(['field', 0, 'subfield'], 'vlaue', ['value', 'other'])
        assert error.__str__() == "WrongValueError: 'field.0.subfield' should be in ['value', 'other'] but got 'vlaue' instead"
        assert error.as_dict() == dict(
            explicit_content='WrongValueError',
            field=['field', 0, 'subfield'],
            received='vlaue',
            expected=['value', 'other']
        )

    def test_wrong_format_error(self):
        error = WrongFormatError(['field', 0, 'subfield'], int, 'float')
        assert error.__str__() == "WrongFormatError: 'field.0.subfield' should be a(n) 'float' but got 'int' instead"
        assert error.as_dict() == dict(
            explicit_content="WrongFormatError",
            field=['field', 0, 'subfield'],
            received=int,
            expected='float'
        )

    def test_wrong_datetime_format_error(self):
        error = WrongDatetimeFormatError(['field', 0, 'subfield'], 'not a datetime', 'date')
        assert error.__str__() == "WrongFormatError: 'field.0.subfield' does not follow the 'date' format, got 'not a datetime'"
        assert error.as_dict() == dict(
            explicit_content="WrongFormatError",
            field=['field', 0, 'subfield'],
            format='date',
            received='not a datetime'
        )

    def test_regex_error(self):
        error = RegexError(['field', 0, 'subfield'], '(0-9)$', 'value')
        assert error.__str__() == "RegexError: 'field.0.subfield' should match pattern '(0-9)$' but got 'value'"
        assert error.as_dict() == dict(
            explicit_content='RegexError',
            field=['field', 0, 'subfield'],
            pattern='(0-9)$',
            value='value'
        )

    def test_empty_string_error(self):
        error = EmptyStringError(['field', 0, 'subfield'])
        assert error.__str__() == "EmptyStringError: 'field.0.subfield' return an empty string"
        assert error.as_dict() == dict(
            explicit_content='EmptyStringError',
            field=['field', 0, 'subfield']
        )

    def test_minlen_error(self):
        error = MinLenghtError(['field', 0, 'subfield'], 0, 5)
        assert error.__str__() == "MinLenghtError: 'field.0.subfield' got 0 values but 5 minimum required"
        assert error.as_dict() == dict(
            explicit_content='MinLenghtError',
            field=['field', 0, 'subfield'],
            received=0,
            expected=5
        )

    def test_maxlen_error(self):
        error = MaxLenghtError(['field', 0, 'subfield'], 5, 0)
        assert error.__str__() == "MaxLenghtError: 'field.0.subfield' got 5 values but 0 maximum required"
        assert error.as_dict() == dict(
            explicit_content='MaxLenghtError',
            field=['field', 0, 'subfield'],
            received=5,
            expected=0
        )


if __name__ == '__main__':
    unittest.main()
