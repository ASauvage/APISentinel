import json


TYPE = [
    'Object',
    'Array',
    'String',
    'Number',
    'Boolean',
    'Null'
]


def recursive_test(path: list, mapping: dict, errors: list) -> list:
    for field_name, field_value in mapping.items():
        value_path = path + [field_name] if field_name != "_tmpfield" else path
        try:
            value_type = field_value['_type']

            if value_type not in TYPE:
                errors.append("UnknownType: type '{}' is not an existing type in field {}".format(value_type, value_path))

            if value_type == 'Object':
                recursive_test(value_path, field_value['_properties'], errors)

            elif value_type == 'Array':
                for index in range(len(field_value['_values'])):
                    recursive_test(value_path + [index], {'_tmpfield':field_value['_values'][index]}, errors)

        except KeyError as e:
            errors.append("RequiredFieldMissing: field {} is required".format(value_path + [e.args[0]]))

    return errors


def integrity_test(mapping_path: str) -> list:
    with open(mapping_path, 'r') as file:
        mapping_json = json.load(file)

        return recursive_test(list(), mapping_json, list())


def response_simulation(path: list, mapping: dict) -> dict:
    response_tmp = dict()
    for field_name, field_value in mapping.items():
        value_path = path + [field_name] if field_name != "_tmpfield" else path
        value_type = field_value['_type']

        if value_type == 'Object':
            response_tmp[field_name] = response_simulation(value_path, field_value['_properties'])

        elif value_type == 'Array':
            value = list()
            for index in range(len(field_value['_values'])):
                value.append(response_simulation(value_path, {'_tmpfield':field_value['_values'][index]})['_tmpfield'])

            response_tmp[field_name] = value

        else:
            response_tmp[field_name] = value_type

    return response_tmp


def simulation_test(mapping_path: str) -> dict:
    with open(mapping_path, 'r') as file:
        mapping_json = json.load(file)

        return response_simulation(list(), mapping_json)


if __name__ == "__main__":
    mapping = "./data/mapping/pokeapi/pokemon.json"

    errors = integrity_test(mapping)

    if errors:
        for error in errors:
            print(error)
    else:
        print("This mapping file is correct")
        with open("./output.json", 'w') as file:
            json.dump(simulation_test(mapping), file, indent=4)

