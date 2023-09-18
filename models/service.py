from data.services_config import SERVICE


class Service:
    """
    Service
    """
    def __init__(self, name: str):
        self.service = SERVICE[name]

    @property
    def path(self) -> str:
        return self.service['path']

    def url(self, env: str, api: str) -> str:
        if self.service['url'][env]:
            return self.service['uri'].format(url=self.service['url'][env], api=api)
        else:
            raise Exception(f"no url defined for {env}")

    @property
    def headers(self) -> dict:
        return self.service['headers'] if 'headers' in self.service.keys() else {}

    @property
    def index_elk(self) -> str:
        return self.service['index_elk']
