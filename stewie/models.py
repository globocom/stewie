# coding: utf-8
'''

Event document, collection `events`

{
 'target'   : 'TARGET-ID',
 'bucket'   : 'BUCKET-ID',
 'metrics'  : {'cpu', 2.5, 'mem': 400, ... },
 'timestamp': 8192819082,
 'is_anomalous': False,
}

`timestamp` is optional, if not supplied the current timestamp is used. Always
UTC timestamp should be used.


Calculus base document.

Data for calculus reference are stored on `calculus_base` collection, there is just
one document with the format:

{'bucket': 'bk1',
 'counters': {
              'metric1': {'total': xx, 'count': yy, 'squared_total': zz },
              'metric2': {'total': aa, 'count': bb, 'squared_total': cc },
             }
}

`total` is the ∑ of all the metric values,
`squared_total` is the ∑ of all
`count` is the amount of events that reported this metric

'''
import time
from datetime import datetime

import pymongo

from stewie.config import settings

conn = pymongo.Connection(settings.DB_HOST)
db = conn[settings.DB_NAME]

def add_event(bucket, target, metrics, timestamp):
    event = {
        'target': target,
        'bucket': bucket,
        'metrics': validate_metrics(metrics),
        'timestamp': validate_timestamp(timestamp),
        'is_anomalous': False,
        }
    db.events.save(event)
    update_calculus_base(event['bucket'], event['metrics'])
    return event

def mark_event_as_anomalous(event):
    db.events.update(event, {'is_anomalous': True})

def find_all_events():
    return db.events.find()

def find_anomalous_events():
    return db.events.find({'is_anomalous': True})

def remove_all_events():
    db.events.remove()


def update_calculus_base(bucket, metrics):
    inc_doc = {}

    for metric, value in metrics.iteritems():
        inc_doc['counters.%s.count' % metric] = 1
        inc_doc['counters.%s.total' % metric] = value
        inc_doc['counters.%s.squared_total' % metric] = value**2

    db.calculus_base.update({'bucket': bucket}, {'$inc': inc_doc}, upsert=True)

def get_calculus_base(bucket):
    cb = db.calculus_base.find_one({'bucket': bucket})
    return {} if not cb else cb.get('counters', {})

def remove_all_calculus_base():
    db.calculus_base.remove()


# validators

class ValidationError(Exception):
    pass

def validate_timestamp(timestamp):
    if not timestamp:
        return datetime.utcnow()
    try:
        return datetime.fromtimestamp(float(timestamp))
    except (TypeError, ValueError):
        raise ValidationError("Invalid timestamp: '%s'" % timestamp)

def validate_metrics(metrics):
    if not metrics:
        raise ValidationError("`metrics` should not be empty")

    # tornado's `request.arguments` is a dict where values are always lists
    # but we don't allow more that one value for a metric

    plain_metrics = {}

    for metric, value in metrics.iteritems():
        if isinstance(value, (list, tuple)):
            if len(value) > 1:
                raise ValidationError("Found duplicate values for metric: '%s'" % metric)
            value = value[0]

        try:
            plain_metrics[metric] = float(value)
        except ValueError:
            raise ValidationError("Metric values should be numbers")

    return plain_metrics
