'''
Tests for external API, where metrics are posted
'''

import requests

from stewie import models
from .helpers import url_to_test


api_url = url_to_test('/api/event')

def setup_function(func):
    models.remove_all_events()

def test_should_return_400_in_invalid_post():
    resp = requests.post(api_url, data={})
    assert 400 == resp.status_code
