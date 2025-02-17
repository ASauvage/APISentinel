import os
import yaml
from time import sleep
from datetime import datetime

from models.tester import apitester
from models.service import Service
from utils.mongodb import MongoCon
from utils.commons import generate_session_id, query_specs_secret


class GlobalTester:
    def __init__(self, env: str, service: str, headers: dict = None):
        if not headers:
            headers = dict()

        self.session_id = generate_session_id()
        self.env = env
        self.service = Service(service)
        self.tests = list()

        print(f"Service: {self.service.name}\nEnv: {self.env}")
        print("Your session ID: " + self.session_id)
        for file in os.listdir('{}/data/mapping/{}'.format(os.getcwd(), self.service.path)):
            if file.endswith('.json'):
                # default specifications
                query_specs = dict(headers=self.service.headers)
                extended_paths = ['']
                yaml_options = dict(save_response=False, valid_http_code=[200])

                if os.path.isfile('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml')):
                    with open('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml'), 'r') as yaml_file:
                        specs = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        extended_paths = specs['extended_paths'] if 'extended_paths' in specs.keys() else extended_paths
                        query_specs = specs['query_specs'] if 'query_specs' in specs.keys() else query_specs
                        query_specs['headers'] = (self.service.headers | query_specs['headers']) if 'headers' in query_specs.keys() else self.service.headers

                        yaml_options['save_response'] = specs['save_response'] if 'save_response' in specs.keys() else False
                        yaml_options['valid_http_code'] = specs['valid_http_code'] if 'valid_http_code' in specs.keys() else [200]
                query_specs['headers'] = query_specs['headers'] | headers

                self.test_executer(filename=file, api=file[:-5], query_specs=query_specs, extended_paths=extended_paths, **yaml_options)

        MongoCon().save_results(self.tests)

        print("\nYour session ID: " + self.session_id)

    def test_executer(self, **specifications):
        specifications['query_specs'], query_specs_hidden = query_specs_secret(specifications['query_specs'])

        for extended_path in specifications['extended_paths']:
            response, errors = apitester(self.env, self.service, extended_path, **specifications)

            self.tests.append(dict(
                test_info=dict(
                    session_id=self.session_id,
                    title=f"Test on /{specifications['api'] + extended_path}",
                    tags=['apitester', self.service.name],
                    version="1.5.0"
                ),
                service=self.service.name,
                env=self.env,
                url=self.service.url(self.env, specifications['api'], extended_path, **specifications['query_specs']['params'] if 'params' in specifications['query_specs'].keys() else {}),
                headers={"User-Agent": "test-mapping", "referer": 'test-mapping', **query_specs_hidden['headers']},
                params=query_specs_hidden['params'] if 'params' in query_specs_hidden.keys() else {},

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
