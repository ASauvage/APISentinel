import json
import os
import json
import yaml
from datetime import datetime
from utils.commons import generate_session_id
from utils.mongodb import MongoCon
from models.tester import apitester
from models.service import Service


class GlobalTester:
    def __init__(self, env: str, service: str):
        self.session_id = generate_session_id()
        self.env = env
        self.service = Service(service)

        self.tests = list()

        print(f"Service: {self.service.name}\nEnv: {self.env}")
        print("Your session ID: " + self.session_id)
        for file in os.listdir('{}/data/mapping/{}'.format(os.getcwd(), self.service.path)):
            if file.endswith('.json'):
                extended_paths = ['']
                query_specs = {'headers': self.service.headers}
                if os.path.isfile('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml')):
                    with open('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml'), 'r') as yaml_file:
                        specs = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        extended_paths = specs['extended_paths'] if 'extended_paths' in specs.keys() else extended_paths
                        query_specs = specs['query_specs'] if 'query_specs' in specs.keys() else query_specs
                        query_specs['headers'] = (self.service.headers | query_specs['headers']) if 'headers' in query_specs.keys() else self.service.headers

                self.test_executer(filename=file, api=file[:-5], query_specs=query_specs, extended_paths=extended_paths)

        MongoCon().save_results(self.tests)

        print("\nYour session ID: " + self.session_id)

    def test_executer(self, **specifications):
        for extended_path in specifications['extended_paths']:
            errors = apitester(self.env, self.service, extended_path, **specifications)

            self.tests.append({
                "title": f"Test on /{specifications['api'] + extended_path}",
                "session_id": self.session_id,
                "env": self.env,
                "service": self.service.name,
                "request": self.service.url(self.env, specifications['api']) + extended_path,
                "headers": {"User-Agent": "test-mapping", "referer": 'test-mapping', **specifications['query_specs']['headers']},
                "params": specifications['query_specs']['data'] if 'data' in specifications['query_specs'].keys() else {},

                "status": False if errors else True,
                "errors": [error.__str__() for error in errors],

                "datetime": int(datetime.now().timestamp())
            })
            print("F" if errors else ".", end='')
