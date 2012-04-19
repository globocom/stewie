'''
Tests for the detector
'''

from stewie.tests import helpers
from stewie.detector import Detector

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
