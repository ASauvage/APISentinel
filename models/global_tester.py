import json
import os
import json
import yaml
from datetime import datetime
from utils.commons import generate_session_id
from models.tester import apitester
from models.service import Service


class GlobalTester:
    def __init__(self, env: str, service: str):
        self.session_id = generate_session_id()
        self.env = env
        self.service = Service(service)

        self.tests = list()

        print("Your session ID: " + self.session_id)
        for file in os.listdir('{}/data/mapping/{}'.format(os.getcwd(), self.service.path)):
            if file.endswith('.json'):
                query_specs = {}
                if os.path.isfile('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml')):
                    with open('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml'), 'r') as yaml_file:
                        query_specs = yaml.load(yaml_file, Loader=yaml.FullLoader)

                self.test_executer(filename=file, api=file[:-5], headers=self.service.headers, query_specs=query_specs)

        with open('{}/data/saved/{}.json'.format(os.getcwd(), self.session_id), 'w') as file:
            json_object = json.dumps(self.tests, ensure_ascii=False, indent=4)
            file.write(json_object)
        print("\nYour session ID: " + self.session_id)

    def test_executer(self, **specifications):
        errors = apitester(self.env, self.service, **specifications)

        self.tests.append({
            "title": f"Mapping test on {specifications['filename']}",
            "env": self.env,
            "service": self.service.name,

            "status": False if errors else True,
            "errors": [error.__str__() for error in errors],

            "request": self.service.url(self.env, specifications['api']),
            "datetime": datetime.now().strftime("%d %b %Y - %H:%M:%S")
        })
        print("F" if errors else ".", end='')
