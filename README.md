# API Tester

This project use Python to test your api with predefined mapping.

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
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if st to `false` and the field is missing
- `_nullable` (optional) a Boolean that defin if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`


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
- `_enums` (optional) an Array containing all enumerations available of this field. Return an `WrongEnumsError` if value isn't in this Array
- `_regex` (optional) A String containing a regular expression pattern. Return `RegexError` if the pattern doesn't match
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if st to `false` and the field is missing
- `_nullable` (optional) a Boolean that defin if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`


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
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if st to `false` and the field is missing
- `_nullable` (optional) a Boolean that defin if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`


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
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if st to `false` and the field is missing
- `_nullable` (optional) a Boolean that defin if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`


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
- `_optional` (optional) a Boolean that define if the field is optional. Return an error of type `MissingFIeldError` if st to `false` and the field is missing
- `_nullable` (optional) a Boolean that defin if the field can be `null`. Return an `WrongValueError` if set to `false` and the field is `null`

### Create your service configuration

In the python file `data/service_config.py`, you can add your service config in the `SERVICE` variable.

```python
SERVICE = {
    "pokeapi": {
            "path": "/pokeapi/",
            "url": {
                "localhost": None,
                "snapshot": None,
                "recette": None,
                "production": "https://pokeapi.co/api/v2/",
            },
            "headers": {},
            "uri": "{url}/{api}/",
    }
}
```

You can then create a new child class in the `shortcut.py` file

```python
class PokeAPIGlobalTester(GlobalTester):
    def __init__(self, env):
        super().__init__(env, "pokeapi")
```

## How to test your API
import the `shortcut` file and call your child class:

```python
from shortcut import PokeAPIGlobalTester


PokeAPIGlobalTester('production')
```

your will get a session ID to find your tests results in mongoDB.
