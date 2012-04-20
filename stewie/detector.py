import math
from stewie import models

EPSILON = 1e-8

class Detector(object):

    def detect_anomaly(self, event):
        return self.calculate_total_probability(event) < EPSILON

    def calculate_total_probability(self, event):
        metrics = self.get_metrics(event)
        probability = 1.0
        for key in metrics:
            probability *= self.calculate_probability_by_metric(key, event)
        return probability

    def calculate_probability_by_metric(self, key, event):
        bucket = self.get_bucket(event)

        try:
            total, n, squared_total = self.fetch_data_from_calculus_base(bucket, key)
        except KeyError:
            '''
            it's the first time that this metric was requested
            '''
            return 1

        variance = self.calculate_variance(total, squared_total, n)
        current_value = self.get_current_value(event, key)
        average = self.calculate_average(total, n)

        probability = self.calculate_probability(current_value, average, variance)
        return probability

    def fetch_data_from_calculus_base(self, bucket, key):
        calculus_base = models.get_calculus_base(bucket)

        total = calculus_base[key]["total"]
        count = calculus_base[key]["count"]
        squared_total = calculus_base[key]["squared_total"]
        return total, count, squared_total

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

    def calculate_probability(self, current_value, average_of_metric, variance):
        if variance == 0:
            return 1

        exponent = -1.0 * math.pow(current_value - average_of_metric, 2) / (2 * variance)

        return 1.0 / (math.sqrt(2*math.pi * variance)) * math.exp(exponent)

    def get_metrics(self, event):
        return event['metrics'].keys()

    def get_current_value(self, event, key):
        return event['metrics'][key]

    def get_bucket(self, event):
        return event['bucket']
