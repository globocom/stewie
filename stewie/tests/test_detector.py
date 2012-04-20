'''
Tests for the detector
'''

from stewie.tests import helpers
from stewie.detector import Detector
from stewie import models
import time

def setup_function(func):
    detector = Detector()
    models.remove_all_events()
    models.remove_all_calculus_base()

def test_detector_should_be_able_to_calculate_variance():
    '''
    variance = (sum(values^2) / n) - average^2
    '''
    occurrences = [1, 2, 3, 4]
    number_of_occurrences = len(occurrences)
    total = sum(occurrences)
    sum_of_square_of_occurrences = sum([pow(number, 2) for number in occurrences])

    detector = Detector()

    assert 1.25 == detector.calculate_variance(total, sum_of_square_of_occurrences, number_of_occurrences)

def test_detector_should_be_able_to_calculate_probability():
    '''
    This probability mathematics was extracted from:
    http://s3.amazonaws.com/mlclass-resources/docs/slides/Lecture15.pdf

    >>> 1/(math.sqrt(math.pi * 2) * 20) * math.exp(-0.5)
    0.01209853622595717
    '''
    current_metric = 80
    avg_of_metric = 100
    variance = 400

    detector = Detector()

    assert round(0.01209853622595717 -
                detector.calculate_probability(current_metric, avg_of_metric, variance), 5) == 0

def test_detector_should_be_able_to_calculate_probability_with_zero_variance():
    detector = Detector()
    assert 1 == detector.calculate_probability(1, 1, 0)

def test_detector_should_be_able_to_calculate_probability_by_metric():
    models.add_event('edge', 'edge_01', {u'cpu': u'2', u'mem': u'10'}, time.time())
    detector = Detector()
    event = helpers.get_fake_event()
    assert 1 == detector.calculate_probability_by_metric("cpu", event)
    assert 1 == detector.calculate_probability_by_metric("mem", event)

def test_detector_should_be_able_to_calculate_total_probability():
    detector = Detector()
    models.add_event('edge', 'edge_01', {u'cpu': u'2', u'mem': u'10'}, time.time())
    event = helpers.get_fake_event()
    cpu_prob = detector.calculate_probability_by_metric("cpu", event)
    mem_prob = detector.calculate_probability_by_metric("mem", event)
    assert cpu_prob * mem_prob == detector.calculate_total_probability(event)

def test_detector_should_be_able_to_detect_anomaly():
    detector = Detector()
    event = helpers.get_fake_event()
    assert False == detector.detect_anomaly(event)

def test_detector_should_be_able_to_fetch_the_metrics_from_event():
    event = helpers.get_fake_event()
    detector = Detector()

    assert sorted(["cpu", "mem"]) == sorted(detector.get_metrics(event))

def test_detector_should_be_able_to_get_current_value():
    detector = Detector()
    event = helpers.get_fake_event()
    assert 2.5 == detector.get_current_value(event, "cpu")
    assert 40 == detector.get_current_value(event, "mem")

def test_detector_should_be_able_to_get_bucket():
    detector = Detector()
    event = helpers.get_fake_event()
    assert 'edge' == detector.get_bucket(event)

def test_detector_should_calculate_probability_for_each_metric(monkeypatch):
    event = helpers.get_fake_event()
    list_of_keys = ['cpu', 'mem']

    def fake_calculate_probability_by_metric(key, event):
        list_of_keys.remove(key)
        return 1

    detector = Detector()
    monkeypatch.setattr(detector, 'calculate_probability_by_metric', fake_calculate_probability_by_metric)
    detector.detect_anomaly(event)

    assert not list_of_keys

def test_detector_should_fetch_calculus_base_of_bucket_and_key():
    models.add_event('edge', 'edge_01', {u'cpu': u'2', u'mem': u'10'}, time.time())
    models.add_event('edge', 'edge_02', {u'cpu': u'3', u'mem': u'20'}, time.time())

    detector = Detector()

    expected = (5, 2, 13)

    assert expected == detector.fetch_data_from_calculus_base("edge", "cpu")

def test_detector_should_be_able_to_calculate_the_number_of_standard_deviations_of_metric():
    # adding this two events will generate a standard deviation of: cpu: 0.5, mem: 5
    models.add_event('edge', 'edge_01', {u'cpu': u'2', u'mem': u'10'}, time.time())
    models.add_event('edge', 'edge_02', {u'cpu': u'3', u'mem': u'20'}, time.time())

    detector = Detector()

    event = {
            'target'   : 'edge_01',
            'bucket'   : 'edge',
            'metrics'  : {'cpu': 4.0, 'mem': 30},
            'timestamp': 8192819082,
            }


    assert 3 == detector.calculate_the_number_of_standard_deviations(event, "cpu")
    assert 3 == detector.calculate_the_number_of_standard_deviations(event, "mem")


