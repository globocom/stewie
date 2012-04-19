
from tornado.web import RequestHandler, HTTPError

from stewie import models, detector

class NewEventHandler(RequestHandler):

    def post(self):
        event = self.parse_event()
        models.add_event(event['target'], event['bucket'], event['metrics'],
                         event['timestamp'])

        self.update_calculus_base(event)
        self.detect_anomaly(event)

    def update_calculus_base(self, event):
        for metric in event['metrics']:
            models.update_calculus_base(metric['metric'], metric['value'])

    def detect_anomaly(self, event):
        anomalies = detector.detect_anomaly(event)
        for anomalies in anomalies:
            models.save_anomaly(anomaly)

    def parse_event(self):
        # FAKED!!
        raise HTTPError(400)
        return {'target': 'foo',
                'bucket': 'bar',
                'metrics': [{'metric': 'cpu', 'value': 1.5}],
                'timestamp': 123456789}

api_urls = [
    (r'/api/event', NewEventHandler),
]
