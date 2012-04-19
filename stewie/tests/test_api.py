'''
Tests for external API, where metrics are posted
'''

import requests

from .helpers import url_to_test

api_url = url_to_test('/api/event')

def test_should_return_200_on_valid_post():
    resp = requests.post(api_url)
    assert 200 == resp.status_code