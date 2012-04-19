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
        'timestamp': validate_timestamp(timestamp)
        }
    db.events.save(event)

def find_all_events():
    return db.events.find()

def remove_all_events():
    db.events.remove()

def update_calculus_base(metric, value):
    pass

def get_calculus_base():
    return {}

def save_anomaly(anomaly):
    pass


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
        if len(value) > 1:
            raise ValidationError("Found duplicate values for metric: '%s'" % metric)

        try:
            plain_metrics[metric] = float(value[0])
        except ValueError:
            raise ValidationError("Metric values should be numbers")

    return plain_metrics
