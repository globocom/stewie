import time

from stewie import models


def setup_function(func):
    models.remove_all_events()
    models.remove_all_calculus_base()


def test_should_update_calculus_base_when_event_created():
    metrics = {u'load': u'2', u'mem': u'150'}

    models.add_event('bk1', 'mach1', metrics, time.time())

    assert_calculus_base_updated('bk1', {u'load': {'total': 2.0,
                                                   'count': 1,
                                                   'squared_total': 4.0},
                                         u'mem': {'total': 150.0,
                                                  'count': 1,
                                                  'squared_total': 22500.0}
                                         })

def test_should_not_duplicate_calculus_base_per_bucket():
    models.add_event('bk1', 'mach1', {u'load': u'2', u'mem': u'10'}, time.time())
    models.add_event('bk1', 'mach2', {u'load': u'3', u'mem': u'20'}, time.time())
    models.add_event('bk1', 'mach3', {u'load': u'4', u'mem': u'30'}, time.time())

    assert_calculus_base_updated('bk1', {u'load': {'total': 9.0,
                                                   'count': 3,
                                                   'squared_total': 29.0},
                                         u'mem': {'total': 60.0,
                                                  'count': 3,
                                                  'squared_total': 1400.0}
                                         })

def test_should_update_calculus_base_on_different_buckets():
    models.add_event('bk1', 'mach1', {u'load': u'2', u'mem': u'10'}, time.time())
    models.add_event('bk2', 'mach2', {u'load': u'3', u'mem': u'20'}, time.time())

    assert_calculus_base_updated('bk1', {u'load': {'total': 2.0,
                                                   'count': 1,
                                                   'squared_total': 4.0},
                                         u'mem': {'total': 10.0,
                                                  'count': 1,
                                                  'squared_total': 100.0}
                                         })
    assert_calculus_base_updated('bk2', {u'load': {'total': 3.0,
                                                   'count': 1,
                                                   'squared_total': 9.0},
                                         u'mem': {'total': 20.0,
                                                  'count': 1,
                                                  'squared_total': 400.0}
                                         })


def assert_calculus_base_updated(bucket, counters):
    assert 1 == models.db.calculus_base.find({'bucket': bucket}).count()
    assert counters == models.get_calculus_base(bucket)
