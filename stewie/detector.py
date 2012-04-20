import math

class Detector(object):

    def detect_anomaly(self, event):
        metrics = self.get_metrics(event)

        for key in metrics: #need tests
            self.calculate_probability_by_metric(key, event)

    def calculate_probability_by_metric(self, key, event):
        bucket = self.get_bucket(event)
        total, n, squared_total = self.fetch_data_from_calculus_base(bucket, key)

        variance = self.calculate_variance(total, squared_total, n)
        current_value = self.get_current_value(event, key)
        average = self.calculate_average(total, n)

        probability = self.calculate_probability(current_value, average, variance)
        return probability

    def fetch_data_from_calculus_base(self, bucket, key): #stub
        calculus_base = {'total': 250, 'count': 100, 'squared_total': 625 }
        return calculus_base['total'], calculus_base['count'], calculus_base['squared_total']

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

        exponent = -1 * math.pow(current_value - average_of_metric, 2) / (2 * variance)

        return 1 / (math.sqrt(2*math.pi * variance)) * math.exp(exponent)

    def get_metrics(self, event):
        return [elem['metric'] for elem in event['metrics']]

    def get_current_value(self, event, key):
        for elem in event['metrics']:
            if elem['metric'] == key:
                return elem['value']

    def get_bucket(self, event): #need tests
        return event['bucket']
