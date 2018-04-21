from concurrent.futures import ThreadPoolExecutor
import requests
import json

class AServerError(Exception):
    pass

def raise_for_status(response):
    try:
        response.raise_for_status()
    except Exception as e:
        raise AServerError(e)

class AServerConnection:
    def __init__(self, server, password):
        self.endpoint = '{}/note'.format(server)
        self.headers = {
            'auth': password,
            'User-Agent': 'A-Server Themral Printer 0.1'
        }
        self.executor = ThreadPoolExecutor()

    @staticmethod
    def _parse_response(response):
        raise_for_status(response)

        parsed_body = response.json()
        try:
            return parsed_body['file']
        except KeyError:
            raise AServerError(
                'Malformed body. Expected key: "file", found: {}'.format(parsed_body)
            )

    def read(self):
        response = requests.get(self.endpoint, headers=self.headers)
        return self._parse_response(response)

    def futures_read(self):
        return self.executor.submit(self.read)

    def write(self, note):
        response = requests.post(
            self.endpoint,
            headers=self.headers,
            data=json.dumps({'file': note})
        )
        return self._parse_response(response)

    def futures_write(self, note):
        return self.executor.submit(self.write, (note,))

    def cleanup(self):
        self.executor.shutdown()


