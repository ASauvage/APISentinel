from models.global_tester import GlobalTester


class PokeAPIGlobalTester(GlobalTester):
    def __init__(self, env: str, headers: dict = None):
        super().__init__(env, "pokeapi", headers)
