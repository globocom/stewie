'''
Tests for external API, where metrics are posted
'''
import time
import json

import requests

from stewie import models
from .helpers import url_to_test


add_metrics = url_to_test('/api/metrics/%(bucket)s/%(target)s')
add_metrics_with_timestamp = url_to_test('/api/metrics/%(bucket)s/%(target)s/%(timestamp)s')

def setup_function(func):
    models.remove_all_events()
    models.remove_all_calculus_base()

def test_should_return_400_on_post_with_empty_body():
    url = add_metrics % {'bucket': 'bk1', 'target': 'mach1'}
    metrics = {}

    assert_invalid_request(url, metrics, '`metrics` should not be empty')

def test_should_return_400_on_post_with_invalid_metric_value():
    url = add_metrics % {'bucket': 'bk1', 'target': 'mach1'}
    metrics = {'foo': 'not a number'}

    assert_invalid_request(url, metrics, 'Metric values should be numbers')

def test_should_return_400_on_post_with_more_than_one_value_for_same_metric():
    url = add_metrics % {'bucket': 'bk1', 'target': 'mach1'}
    metrics = {'foo': ['12', '13']}

    assert_invalid_request(url, metrics, "Found duplicate values for metric: 'foo'")

def test_should_return_400_on_post_with_invalid_timestamp():
    url = add_metrics_with_timestamp % {'bucket': 'bk1', 'target': 'mach1', 'timestamp': 'invalid'}
    metrics = {'foo': '12'}

    assert_invalid_request(url, metrics, "Invalid timestamp: 'invalid'")

def test_should_return_400_on_post_with_timestamp_out_of_range():
    url = add_metrics_with_timestamp % {'bucket': 'bk1', 'target': 'mach1', 'timestamp': 999999999999999999999}
    metrics = {'foo': '30'}

    assert_invalid_request(url, metrics, "Invalid timestamp: '999999999999999999999'")

def test_should_save_event_if_valid_request():
    url = add_metrics % {'bucket': 'bk1', 'target': 'mach1'}
    metrics = {u'load': u'2', u'mem': u'150'}

    resp = requests.post(url, data=metrics)

    assert 200 == resp.status_code
    assert_event_created('bk1', 'mach1', {u'load': 2, u'mem': 150.0}, time.time())

def test_should_save_event_if_valid_request_with_timestamp():
    metrics = {u'load': u'1.2', u'mem': u'530'}
    timestamp = time.time() - 500
    url = add_metrics_with_timestamp % {'bucket': 'bk1', 'target': 'mach1', 'timestamp': timestamp}

    resp = requests.post(url, data=metrics)

    assert 200 == resp.status_code
    assert_event_created('bk1', 'mach1', {u'load': 1.2, u'mem': 530.0}, timestamp)



# custom asserts

def assert_event_created(bucket, target, metrics, timestamp):
    events = list(models.find_all_events())
    assert 1 == len(events)

    assert bucket == events[0]['bucket']
    assert target == events[0]['target']
    assert metrics == events[0]['metrics']
    assert timestamp - time.mktime(events[0]['timestamp'].timetuple()) <= 1


def assert_invalid_request(url, metrics, error_message=None):
    resp = requests.post(url, data=metrics)

    assert 400 == resp.status_code
    assert 'application/json; charset=UTF-8' == resp.headers['Content-Type']
    if error_message:
        assert error_message == json.loads(resp.content)['error_message']
    assert 0 == len(list(models.find_all_events()))
