import requests
from xml_dict import xml_to_dict

class FMS(object):
    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def _call_api(self, method, **kwargs):
        url = "http://{server}:{port}/admin/{method}".format(
            server=self.server,
            port=self.port,
            method=method)
        kwargs.setdefault('auser', self.username)
        kwargs.setdefault('apswd', self.password)
        response = requests.get(url, params=kwargs)
        xml_dict = xml_to_dict(response.content)

        if xml_dict['level'] == 'error':
            raise ValueError(xml_dict['description'])

        return xml_dict

    def getServerStats(self):
        return self._call_api('getServerStats')
