import math

class Detector(object):
    def calculate_variance(self, total, squared_total, count):
        '''
        total: the sum of all values
        squared_total: the sum of all squared values
        count: the number of occurrences o
        '''
        average = float(total) / count

        return (float(squared_total)/count) - pow(average, 2)

