'''
Tests for the detector
'''

from stewie.tests import helpers
from stewie.detector import Detector

def setup_function(func):
    detector = Detector()

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
    detector = Detector()
    event = helpers.get_fake_event()
    assert 1 == detector.calculate_probability_by_metric("cpu", event)
    assert 1 == detector.calculate_probability_by_metric("mem", event)

def test_detector_should_be_able_to_detect_anomaly():
    detector = Detector()
    event = helpers.get_fake_event()
    cpu_prob = detector.calculate_probability_by_metric("cpu", event)
    mem_prob = detector.calculate_probability_by_metric("mem", event)
    assert cpu_prob * mem_prob == detector.detect_anomaly(event)

def test_detector_should_be_able_to_fetch_the_metrics_from_event():
    event = helpers.get_fake_event()
    detector = Detector()

    assert ["cpu", "mem"] == detector.get_metrics(event)

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

