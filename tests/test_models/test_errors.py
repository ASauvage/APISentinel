import unittest
from models.errors import *


class TestErrors(unittest.TestCase):
    def test_error(self):
        error = Error()
        assert error.__str__() == "UnknownError: Unexpected error occured"
        assert error.as_dict() == dict(
            explicit_content='UnknownError'
        )

    def test_missing_field_error(self):
        error = MissingFieldError('field')
        assert error.__str__() == "MissingFieldError: field 'field' is missing"
        assert error.as_dict() == dict(
            explicit_content='MissingFieldError',
            field='field'
        )

    def test_wrong_type_error(self):
        error = WrongTypeError('field', str, int)
        assert error.__str__() == "WrongTypeError: 'field' should be a(n) <class 'int'> not <class 'str'>"
        assert error.as_dict() == dict(
            explicit_content='WrongTypeError',
            field='field',
            received=str,
            expected=int
        )

    def test_wrong_value_error(self):
        error = WrongValueError('field', 'vlaue', ['value', 'other'])
        assert error.__str__() == "WrongValueError: 'field' should be in ['value', 'other'] but got 'vlaue' instead"
        assert error.as_dict() == dict(
            explicit_content='WrongValueError',
            field='field',
            received='vlaue',
            expected=['value', 'other']
        )

    def test_regex_error(self):
        error = RegexError('field', '(0-9)$')
        assert error.__str__() == "RegexError: 'field' should match pattern '(0-9)$'"
        assert error.as_dict() == dict(
            explicit_content='RegexError',
            field='field',
            pattern='(0-9)$'
        )

    def test_minlen_error(self):
        error = MinLenghtError('field', 0, 5)
        assert error.__str__() == "MinLenghtError: 'field' got 0 values but 5 minimum required"
        assert error.as_dict() == dict(
            explicit_content='MinLenghtError',
            field='field',
            received=0,
            expected=5
        )

    def test_maxlen_error(self):
        error = MaxLenghtError('field', 5, 0)
        assert error.__str__() == "MaxLenghtError: 'field' got 5 values but 0 maximum required"
        assert error.as_dict() == dict(
            explicit_content='MaxLenghtError',
            field='field',
            received=5,
            expected=0
        )
