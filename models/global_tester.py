import os

from utils.commons import generate_session_id
from models.tester import apitester
from models.service import Service


class GlobalTester:
    def __init__(self, env: str, service: str):
        self.session_id = generate_session_id()
        self.env = env
        self.service = Service(service)

        self.tests = list()

        for file in os.listdir('{}/data/mapping/{}'.format(os.getcwd(), self.service.path)):
            self.test_executer(filename=file, api=file[:-5])

        # FixMe elk request


    def test_executer(self, **specifications):
        errors = apitester(self.env, self.service, **specifications)

        self.tests.append({
            "title": f"Mapping test on {specifications['filename']}",
            "env": self.env,
            "service": "pokeapi",

            "status": False if errors else True,
            "errors": [error.__str__() for error in errors],

            "request": self.service.url(self.env, specifications['api']),
        })
