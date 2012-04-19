import requests

def post(stewie_server, bucket, target, timestamp=None, **kwargs):
    url = '/'.join([stewie_server, 'api/metrics', bucket, target])
    requests.post(url, data=kwargs)
