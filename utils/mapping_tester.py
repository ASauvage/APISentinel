import os
import json

# What it should do
# - build response from mapping
# - return errors if there are


def integrity_test(mapping_path: str) -> list:
    errors = list()

    mapping = get_mapping(mapping_path)

    # todo check fields properties (warning for aditional)

    return errors


def simulation_test(mapping_path: str) -> dict:
    mapping = get_mapping(mapping_path)

    def simulate_field(path: list, mapping: dict) -> dict:
        response_tmp = dict()
        for field_name, field_value in mapping.items():
            value_path = path + [field_name] if field_name != "_tmpfield" else path
            value_type = field_value['_type']

            if value_type == 'Object':
                try:
                    response_tmp[field_name] = simulate_field(value_path, field_value['_properties'])
                except KeyError:
                    response_tmp[field_name] = dict()
            elif value_type == 'Array':
                value = list()
                try:
                    for index in range(len(field_value['_values'])):
                        value.append(simulate_field(value_path, {'_tmpfield': field_value['_values'][index]})['_tmpfield'])

                    response_tmp[field_name] = value
                except KeyError:
                    response_tmp[field_name] = list()
            else:
                response_tmp[field_name] = f"{value_type}/{field_value['_format']}" if '_format' in field_value.keys() else value_type

        return response_tmp

    return simulate_field([], mapping)['__unamed__']


def get_mapping(mapping_path: str) -> dict:
    if not mapping_path.endswith('.json'):
        mapping_path += '.json'
    with open('{}/data/mapping/{}'.format(os.getcwd(), mapping_path), 'r') as file:
        return {"__unamed__": json.load(file)}
