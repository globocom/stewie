import json

TEST_HOST = 'http://localhost:7766'

def url_to_test(path):
    return TEST_HOST + path

def get_fake_event():
    return {
            'target'   : 'edge_01',
            'bucket'   : 'edge',
            'metrics'  : {'cpu': 2.5, 'mem': 40},
            'timestamp': 8192819082,
            }

def get_fake_calculus_base(event_bucket):
    return {'cpu': {'total': 300, 'count': 100, 'squared_total': 600 },
            'mem': {'total': 5000, 'count': 100, 'squared_total': 150000 }}
