import unittest
import json
from os import getcwd
from unittest.mock import patch
from utils.mapping_tester import integrity_test, simulation_test


def mapping(mapping_path):
    with open('tests/test_utils/test_mapping.json', 'r') as file:
        return {"__unamed__": json.load(file)}


class TestMappingTester(unittest.TestCase):
    def test_integrity_test_success(self):
        pass  # todo

    def test_integrity_test_failure(self):
        pass  # todo

    @patch('utils.mapping_tester.get_mapping', side_effect=mapping)
    def test_simulation_test(self, mockpatch):
        response = simulation_test('test/test')
        assert response == [dict(
            metadata=dict(
                request_id="Number/int",
                optional_field="Boolean",
                nullable_field="Boolean",
                datetime="String/datetime"
            ),
            data=["String"],
            enums="String"
        )]


if __name__ == '__main__':
    unittest.main()
