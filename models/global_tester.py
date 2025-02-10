import os
import yaml
from time import sleep
from datetime import datetime
from utils.commons import generate_session_id
from utils.mongodb import MongoCon
from models.tester import apitester
from models.service import Service


class GlobalTester:
    def __init__(self, env: str, service: str, headers: dict = None):
        self.session_id = generate_session_id()
        self.env = env
        self.service = Service(service)

        self.tests = list()

        if not headers:
            headers = {}

        print(f"Service: {self.service.name}\nEnv: {self.env}")
        print("Your session ID: " + self.session_id)
        for file in os.listdir('{}/data/mapping/{}'.format(os.getcwd(), self.service.path)):
            if file.endswith('.json'):
                extended_paths = ['']
                save_response = False
                query_specs = {'headers': self.service.headers}
                if os.path.isfile('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml')):
                    with open('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml'), 'r') as yaml_file:
                        specs = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        extended_paths = specs['extended_paths'] if 'extended_paths' in specs.keys() else extended_paths
                        query_specs = specs['query_specs'] if 'query_specs' in specs.keys() else query_specs
                        query_specs['headers'] = (self.service.headers | query_specs['headers']) if 'headers' in query_specs.keys() else self.service.headers
                        save_response = specs['save_response'] if 'save_response' in specs.keys() else False
                query_specs['headers'] = query_specs['headers'] | headers

                self.test_executer(filename=file, api=file[:-5], query_specs=query_specs, extended_paths=extended_paths, save_response=save_response)

        MongoCon().save_results(self.tests)

        print("\nYour session ID: " + self.session_id)

    def test_executer(self, **specifications):
        for extended_path in specifications['extended_paths']:
            response, errors = apitester(self.env, self.service, extended_path, **specifications)

            self.tests.append(dict(
                test_info=dict(
                    session_id=self.session_id,
                    title=f"Test on /{specifications['api'] + extended_path}",
                    tags=['apitester', self.service.name]
                ),
                service=self.service.name,
                env=self.env,
                url=self.service.url(self.env, specifications['api'], extended_path, **specifications['query_specs']['params'] if 'params' in specifications['query_specs'].keys() else {}),
                headers={"User-Agent": "test-mapping", "referer": 'test-mapping', **specifications['query_specs']['headers']},
                params=specifications['query_specs']['params'] if 'params' in specifications['query_specs'].keys() else {},

                status=False if errors else True,
                errors=[error.__str__() for error in errors],
                api_response=response,

                timestamp=int(datetime.now().timestamp())
            ))
            print("F" if errors else ".", end='')
            try:
                sleep(self.service.options['request_delay'] * 0.001)
            except KeyError:
                pass
