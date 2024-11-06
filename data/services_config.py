# Add service information here ('{api}' in uri is the api name)

SERVICE = {
    "pokeapi": {
        "path": "/pokeapi/",
        "url": {
            "localhost": None,
            "snapshot": None,
            "recette": None,
            "production": "https://pokeapi.co/api/v2",
        },
        "headers": {},
        "options": {
            "request_delay": 100
        },
        "uri": "{url}/{api}"
    }
}
