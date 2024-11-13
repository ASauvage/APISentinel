# API Tester

This project use Python to test your api with predefined mapping.

## Requirements
- Python 3.9 or higher
- MongoDB server (url customisable in `utils/mongodb.py`)

## How to set up
### Create your mapping

First you have to create a JSON file named the same as your api service:
>exemple: if your request URL is `{url}/pokemon/`, then you have to named your file `pokemon.json`

You have to put your mappings in `data/mapping/your_service_folder/`.
Once the JSON file created, you have to define your API response in it.
All following JSON object are suported by the tester:

- `Number`
- `String`
- `Boolean`
- `Object`
- `Array`
- `Null`

#### Number type
To define a field of type `Number`: 

```json
{
    "field": {
        "_type": "Number"
    }
}
```

These properties are avalaible for `Number` field: 

- `_type` a String that define the type of field (here `Number`). Return `WrongTypeValue` if the type doesn't match
- `_format` (optional) a String that define the type format of field (can be `int`, `float` or `double`)
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if set to `false` and the field is missing
- `_nullable` (optional) a Boolean that define if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`


#### String type
To define a field of type `String`: 

```json
{
    "field": {
        "_type": "String"
    }
}
```

These properties are avalaible for `String` field: 

- `_type` a String that define the type of field (here `String`). Return `WrongTypeValue` if the type doesn't match
- `_format` (optional) a String that define the type format of field (can be `datetime`, `date` or `time`)
- `_enums` (optional) an Array containing all enumerations available of this field. Return an `WrongEnumsError` if value isn't in this Array
- `_regex` (optional) A String containing a regular expression pattern. Return `RegexError` if the pattern doesn't match
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if set to `false` and the field is missing
- `_nullable` (optional) a Boolean that define if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`


#### Boolean type
To define a field of type `Boolean`: 

```json
{
    "field": {
        "_type": "Boolean"
    }
}
```

These properties are avalaible for `Boolean` field: 

- `_type` a String that define the type of field (here `Boolean`). Return `WrongTypeValue` if the type doesn't match
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if set to `false` and the field is missing
- `_nullable` (optional) a Boolean that define if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`


#### Object type
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

These properties are avalaible for `Object` field:

- `_type` a String that define the type of field (here `Object`). Return `WrongTypeValue` if the type doesn't match
- `_properties` an Object containing all properties of this Object. All this field will be tested and matching error will be returned
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if set to `false` and the field is missing
- `_nullable` (optional) a Boolean that define if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`


#### Array type
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

These properties are avalaible for `Array` field:

- `_type` a String that define the type of field (here `Array`). Return `WrongTypeValue` if the type doesn't match
- `_values` an Array containing all possible values of this Array. All this value will be tested and matching error will be returned
- `_minlen` (optional) an Integer that define minimal lenght of this Array 
- `_maxlen` (optional) an Integer that define maximal lenght of this Array
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if set to `false` and the field is missing
- `_nullable` (optional) a Boolean that define if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`

---------

You have to start with unamed field in your json file
```json
{
    "_type": "Array",
    "_values": [
        {
            "_type": "Object",
            "_properties": {}
        }
    ]
}
```

### Create your service configuration

In the python file `data/service_config.py`, you can add your service config in the `SERVICE` variable.

```python
SERVICE = {
    "pokeapi": {
            "path": "/pokeapi/",                            # path to your folder (from `data/mapping`)
            "url": {                                        # server urls of your api
                "localhost": None,
                "snapshot": None,
                "recette": None,
                "production": "https://pokeapi.co/api/v2/",
            },
            "headers": {},                                  # (optional) headers used when your api are requested (can be setup in yaml too)
            "options": {                                    # (optional) options used during tests
                "request_delay": 100                        # (optional) delay between requests in milliseconds
            },
            "uri": "{url}/{api}/",                          # uri build ('{api}' in uri is the api name)
    }
}
```

You can then create a new child class in the `shortcut.py` file
```python
from models.global_tester import import GlobalTester

class PokeAPIGlobalTester(GlobalTester):
    def __init__(self, env):
        super().__init__(env, "pokeapi", **kwargs)
```

#### Create endpoint's specifications
You can create a YAML file with the same name and location of your mapping file to use some specification with tests.
```yaml
extended_path:  # extend path for your API's url
    - '/charizard'
    - '/bulbasaur'

query_specs:  # kwargs for request library (get)
    headers:
        token: 'mon_token'
```

Each path attribute are optional, even the YAML file itself!

## How to test your API
import the `shortcut` file and call your child class:

```python
from shortcut import PokeAPIGlobalTester


PokeAPIGlobalTester('production', headers={'specHeader': '1234'})
```

> You can specify headers child class arguments.

your will get a session ID to find your tests results in mongoDB.

**You can use [ApiTester Dashboard](https://github.com/ASauvage/ApiTester_Dashboard) to analyze the results.** 
