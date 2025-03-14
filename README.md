![APISentinel](APISentinel.png)

This project uses Python to test your API with predefined mappings.

> [!WARNING] 
> Currently, APISentinel only supports JSON format and will return a `NotJsonError` error if this is not the case

## Requirements

- Python 3.9 or higher
- MongoDB server (URL customizable in `utils/mongodb.py`)

## Setup

### Create Your Mapping

First, you need to create a JSON file named after your API service:

> Example: If your request URL is `{url}/pokemon/`, then you must name your file `pokemon.json`.

Your mappings should be placed in `data/mapping/your_service_folder/`.
Once the JSON file is created, you must define your API response in it.
The tester supports the following JSON object types:

- `Number`
- `String`
- `Boolean`
- `Object`
- `Array`
- `Null`

#### Number Type
To define a field of type `Number`:

```json
{
    "field": {
        "_type": "Number"
    }
}
```

Available properties for `Number` fields:

- `_type`: A string defining the field type (`Number`). Returns `WrongTypeValue` if the type does not match.
- `_$ref` (optional): A string containing the name of a generic object (see Generics).
- `_format` (optional): A string defining the field format (`int`, `float`, or `double`).
- `_optional` (optional): A boolean defining whether the field is optional. Returns a `MissingFieldError` if set to `false` and the field is missing.
- `_nullable` (optional): A boolean defining whether the field can be `null`. Returns a `WrongValueError` if set to `false` and the field is `null`.

#### String Type
To define a field of type `String`:

```json
{
    "field": {
        "_type": "String"
    }
}
```

Available properties for `String` fields:

- `_type`: A string defining the field type (`String`). Returns `WrongTypeValue` if the type does not match.
- `_$ref` (optional): A string containing the name of a generic object (see Generics).
- `_format` (optional): A string defining the format (`datetime`, `date`, or `time`).
- `_enums` (optional): An array of valid enumerations. Returns a `WrongEnumsError` if the value is not in this array.
- `_regex` (optional): A string containing a regex pattern. Returns `RegexError` if the pattern does not match.
- `_allow_empty` (optional): A boolean defining whether the string can be empty. Returns `EmptyStringError` if set to `false` and the field is empty.
- `_optional` (optional): A boolean defining whether the field is optional. Returns `MissingFieldError` if set to `false` and the field is missing.
- `_nullable` (optional): A boolean defining whether the field can be `null`. Returns `WrongValueError` if set to `false` and the field is `null`.

#### Boolean Type
To define a field of type `Boolean`:

```json
{
    "field": {
        "_type": "Boolean"
    }
}
```

Available properties for `Boolean` fields:

- `_type`: A string defining the field type (`Boolean`). Returns `WrongTypeValue` if the type does not match.
- `_$ref` (optional): A string containing the name of a generic object (see Generics).
- `_optional` (optional): A boolean defining whether the field is optional. Returns `MissingFieldError` if set to `false` and the field is missing.
- `_nullable` (optional): A boolean defining whether the field can be `null`. Returns `WrongValueError` if set to `false` and the field is `null`.

#### Object Type
To define a field of type `Object`:

```json
{
    "field": {
        "_type": "Object",
        "_properties": {
            "sub_field": {
                "_type": "String"
            }
        }
    }
}
```

Available properties for `Object` fields:

- `_type`: A string defining the field type (`Object`). Returns `WrongTypeValue` if the type does not match.
- `_$ref` (optional): A string containing the name of a generic object (see Generics).
- `_properties`: An object containing all properties of this object.
- `_optional` (optional): A boolean defining whether the field is optional.
- `_nullable` (optional): A boolean defining whether the field can be `null`.

#### Array Type
To define a field of type `Array`:

```json
{
    "field": {
        "_type": "Array",
        "_values": [
            {
                "_type": "String"
            }
        ]
    }
}
```

Available properties for `Array` fields:

- `_type`: A string defining the field type (`Array`). Returns `WrongTypeValue` if the type does not match.
- `_$ref` (optional): A string containing the name of a generic object (see Generics).
- `_values`: An array defining the expected structure of elements in the array.
- `_minlen` (optional): An integer defining the minimum length of the array.
- `_maxlen` (optional): An integer defining the maximum length of the array.
- `_optional` (optional): A boolean defining whether the field is optional.
- `_nullable` (optional): A boolean defining whether the field can be `null`.

### Using Generics and `_$ref`

You can create generic objects by adding mapping files in the `generics` folder inside your service's folder.
This allows you to reference predefined structures in your field specifications.

Example:

```json
{
    "_type": "Object",
    "_properties": {
        "reference": {
            "_optional": true,
            "_$ref": "reference_object"
        }
    }
}
```

This means that the `reference` field will use the structure defined in `reference_object.json` within the `generics` folder.

### Create Your Service Configuration

In `data/service_config.py`, add your service configuration in the `SERVICE` variable:

```python
SERVICE = {
    "pokeapi": {
        "path": "/pokeapi/",        # Path to your folder (from `data/mapping`)
        "url": {                    # API server URLs
            "localhost": None,
            "snapshot": None,
            "recette": None,
            "production": "https://pokeapi.co/api/v2/",
        },
        "headers": {},              # (Optional) Headers used when requesting your API
        "options": {                # (Optional) Options used during tests
            "request_delay": 100    # (Optional) Delay between requests in milliseconds
        },
        "uri": "{url}/{api}/",      # URI structure ('{api}' represents the API name)
    }
}
```

You can then create a new child class in the `shortcut.py` file
```python
from models.global_tester import GlobalTester
class PokeAPIGlobalTester(GlobalTester):
    def __init__(self, env, **kwargs):
        super().__init__(env, "pokeapi", **kwargs)
```

#### Create endpoint's specifications
You can create a YAML file with the same name and location of your mapping file to use some specification with tests.
```yaml
save_response: yes          # save API's response in tests results
save_response_on_error: yes # save API's response only if at least on error is returned (if save_response is set to true, save anyway)
valid_http_code:            # define which http code must not return an error (only code 200 will not return an error by default)
    - 200
extended_path:              # extend path for your API's url
    - '/charizard'
    - '/bulbasaur'
query_specs:                # kwargs for request library (get)
    headers:
        token: '$secret:mon_token'
    params:
        id: 2
```
Each path attribute are optional, even the YAML file itself!

If you have credentials you don't want saved in the database, prefix any headers or parameters value with `$secret:`.

### Run API Tests

Import the `shortcut` file and call your child class:

```python
from shortcut import PokeAPIGlobalTester

PokeAPIGlobalTester('production', headers={'specHeader': '1234'})
```

This will generate a session ID to find your test results in MongoDB.

**You can use [APISentinel Dashboard](https://github.com/ASauvage/APISentinel_Dashboard) to analyze the results.**

