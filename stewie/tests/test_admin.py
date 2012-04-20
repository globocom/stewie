import time

import requests

from stewie import models
from .helpers import url_to_test

admin = url_to_test('/')

def test_admin_should_list_anomalous_events():
    create_anomalous_event('bk1', 'mach1', {'mem': 100, 'load': 2.3}, time.time())
    create_anomalous_event('bk1', 'mach2', {'mem': 100, 'load': 2.3}, time.time())
    create_anomalous_event('bk2', 'mach10', {'mem': 200, 'load': 1.0}, time.time())
    create_anomalous_event('bk2', 'mach20', {'mem': 300, 'load': 1.3}, time.time())

    resp = requests.get(admin)

    assert 200 == resp.status_code
    assert 'mach20' in resp.content
    assert 'bk1' in resp.content

def create_anomalous_event(*args):
    event = models.add_event('bk1', 'mach1', {'mem': 100, 'load': 2.3}, time.time())
    models.mark_event_as_anomalous(event)
