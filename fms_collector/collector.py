from client import post
from fms import FMS

STEWIE_SERVER = 'http://server'
BUCKET = 'fms'

def collect(server, port, username, password):
    s = FMS(server, port, username, password)
    status = s.getServerStats()
    metrics = {
        'total_threads': status['data']['io']['total_threads']
    }
    post(STEWIE_SERVER, BUCKET, target=server, **metrics)
