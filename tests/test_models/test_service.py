import unittest
from models.service import Service


class TestService(unittest.TestCase):
    def test_service(self):
        service = Service('pokeapi')
        assert service.name == 'pokeapi'
        assert service.path == '/pokeapi/'
        assert service.options == dict(request_delay=100)
        assert service.url('production', 'test', '/extra_path', param1=2, param2=1) == "https://pokeapi.co/api/v2/test/extra_path/?param1=2&param2=1"
        assert service.headers == dict()

        assert service.service == dict(
            path="/pokeapi/",
            url=dict(localhost=None, snapshot=None, recette=None, production="https://pokeapi.co/api/v2"),
            headers=dict(),
            options=dict(request_delay=100),
            uri="{url}/{api}"
        )


if __name__ == '__main__':
    unittest.main()
