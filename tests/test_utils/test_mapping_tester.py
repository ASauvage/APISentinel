import unittest
import json
from unittest.mock import patch
from utils.mapping_tester import simulation_test


def mapping(mapping_path):
    with open('tests/test_utils/test_mapping.json', 'r') as file:
        return {"__unamed__": json.load(file)}


class TestMappingTester(unittest.TestCase):
    @patch('utils.mapping_tester.get_mapping', side_effect=mapping)
    def test_simulation_test(self, mockpatch):
        response = simulation_test('test/test')
        assert response == [dict(
            metadata=dict(
                request_id="Number/int",
                not_empty_field="String",
                optional_field="Boolean",
                nullable_field="Boolean",
                datetime="String/datetime"
            ),
            data=["String"],
            enums="String"
        )]


if __name__ == '__main__':
    unittest.main()
