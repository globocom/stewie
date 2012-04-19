# coding: utf-8
'''

Event model

{
 'target'   : 'TARGET-ID',
 'bucket'   : 'BUCKET-ID',
 'metrics'  : [ {'metric': 'cpu', 'value': 2.5 },
                {'metric': 'mem', 'value': 400 },
                .
                .
              ],
 'timestamp': 8192819082,
}

`timestamp` is optional, if not supplied the current timestamp is used. Always
UTC timestamp should be used.


Data for calculus reference are stored on `calculus_base` collection, there is just
one document with the format:

{ 'metrics': [
               {'metric1': {'total': xx, 'count': yy, 'squared_total': zz } },
               {'metric2': {'total': aa, 'count': bb, 'squared_total': cc } },
               .
               .
             ]
}

`total` is the ∑ of all the metric values,
`squared_total` is the ∑ of all
`count` is the amount of events that reported this metric

'''
import pymongo

from stewie.config import settings

conn = pymongo.Connection(settings.DB_HOST)
db = conn[settings.DB_NAME]

def add_event(target, bucket, metrics, timestamp=None):
    pass

def find_all_events():
    ''' Too slow... only used for tests '''
    []

def remove_all_events():
    db.events.remove()

def update_calculus_base(metric, value):
    pass

def get_calculus_base():
    return {}

def save_anomaly(anomaly):
    pass
