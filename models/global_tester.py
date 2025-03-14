import os
import yaml
from time import sleep
from datetime import datetime

from .tester import apitester
from .service import Service
from .results_manager import results_manager
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
                yaml_options = dict(
                    save_response=False,
                    save_response_on_error=False,
                    valid_http_code=[200]
                )

                if os.path.isfile('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml')):
                    with open('{}/data/mapping/{}/{}'.format(os.getcwd(), self.service.path, file[:-4] + 'yaml'), 'r') as yaml_file:
                        specs = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        extended_paths = specs['extended_paths'] if 'extended_paths' in specs.keys() else extended_paths
                        query_specs = specs['query_specs'] if 'query_specs' in specs.keys() else query_specs
                        query_specs['headers'] = (self.service.headers | query_specs['headers']) if 'headers' in query_specs.keys() else self.service.headers

                        yaml_options['save_response'] = specs['save_response'] if 'save_response' in specs.keys() else False
                        yaml_options['save_response_on_error'] = specs['save_response_on_error'] if 'save_response_on_error' in specs.keys() else False
                        yaml_options['valid_http_code'] = specs['valid_http_code'] if 'valid_http_code' in specs.keys() else [200]
                query_specs['headers'] = query_specs['headers'] | headers

                self.test_executer(filename=file, api=file[:-5], query_specs=query_specs, extended_paths=extended_paths, **yaml_options)

        results_manager(self.tests)

        print("\nYour session ID: " + self.session_id)

    def test_executer(self, **specifications):
        specifications['query_specs'], query_specs_hidden = query_specs_secret(specifications['query_specs'])

        for extended_path in specifications['extended_paths']:
            response, errors = apitester(self.env, self.service, extended_path, **specifications)

            self.tests.append(dict(
                title=f"Test on /{specifications['api'] + extended_path}",
                test_info=dict(
                    session_id=self.session_id,
                    service=self.service.name,
                    env=self.env,
                    tags=['apitester', self.service.name],
                    version="1.6.1"
                ),
                url=self.service.url(self.env, specifications['api'], extended_path, **specifications['query_specs']['params'] if 'params' in specifications['query_specs'].keys() else {}),
                headers={"User-Agent": "test-mapping", "referer": 'test-mapping', **query_specs_hidden['headers']},
                params=query_specs_hidden['params'] if 'params' in query_specs_hidden.keys() else {},

                status=False if errors else True,
                errors_list=[error.__str__() for error in errors],
                api_response=response,

                timestamp=int(datetime.now().timestamp())
            ))
            print("F" if errors else ".", end='')
            try:
                sleep(self.service.options['request_delay'] * 0.001)
            except KeyError:
                pass
