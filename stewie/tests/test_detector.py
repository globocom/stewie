'''
Tests for the detector
'''

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
