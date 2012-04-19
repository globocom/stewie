from client import post
from fms import FMS

STEWIE_SERVER = 'http://server'
BUCKET = 'fms'
METRIC_KEYS = [
    'bw_in',
    'bw_out',
    'connected',
    'rtmp_connects',
    'rtmfp_connects',
    'normal_connects',
    'virtual_connects',
    'group_connects',
    'service_connects',
    'service_requests',
    'admin_connects',
    'debug_connects',
    'total_threads',
    'working_threads',
]


def collect(server, port, username, password):
    s = FMS(server, port, username, password)
    status = s.getServerStats()
    metrics = {key: status['data']['io'][key] for key in METRIC_KEYS}
    post(STEWIE_SERVER, BUCKET, target=server, **metrics)
