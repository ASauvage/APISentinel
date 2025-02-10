from data.services_config import SERVICE


class Service:
    """
    Service
    """
    def __init__(self, name: str):
        self.name = name
        self.service = SERVICE[name]

    @property
    def path(self) -> str:
        return self.service['path']

    @property
    def options(self) -> dict:
        return self.service['options'] if 'options' in self.service.keys() else {}

    def url(self, env: str, api: str, extended_path: str = None, **kwargs) -> str:
        if not extended_path:
            extended_path = ''
        url = self.service['uri'].format(url=self.service['url'][env], api=api) + extended_path
        if kwargs:
            url += '/?' + '&'.join([f'{key}={value}' for key, value in kwargs.items()])

        if self.service['url'][env]:
            return url
        else:
            raise Exception(f"no url defined for {env}")

    @property
    def headers(self) -> dict:
        return self.service['headers'] if 'headers' in self.service.keys() else {}
