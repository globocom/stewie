import math

class Detector(object):
    def calculate_variance(self, total, squared_total, count):
        '''
        total: the sum of all values
        squared_total: the sum of all squared values
        count: the number of occurrences o
        '''
        average = self.calculate_average(total, count)

        return (float(squared_total)/count) - pow(average, 2)

    def calculate_average(self, numerator, denominator):
        return float(numerator)/float(denominator)

    def calculate_probability(self, current_metric, average_of_metric, variance):
        exponent = -1 * math.pow(current_metric - average_of_metric, 2) / (2 * variance)

        return 1 / (math.sqrt(2*math.pi * variance)) * math.exp(exponent)

    def get_metrics(self, event):
        return [elem['metric'] for elem in event['metrics']]
