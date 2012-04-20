from tornado.web import RequestHandler, HTTPError

from stewie import models
from stewie.detector import Detector

class AddMetricsHandler(RequestHandler):

    API_ERROR_CODES = 400,

    def initialize(self):
        self.detector = Detector()

    def post(self, bucket, target, timestamp=None):
        event = self.create_event(bucket, target, self.request.arguments, timestamp)
        if self.detector.detect_anomaly(event):
            models.mark_event_as_anomalous(event)

    def create_event(self, *args, **kwargs):
        try:
            return models.add_event(*args, **kwargs)
        except models.ValidationError as ex:
            raise HTTPError(400, str(ex))

    def detect_anomaly(self, event):
        detector = Detector()
        return detector.detect_anomaly(event)

    def write_error(self, status_code, **kwargs):
        if status_code in self.API_ERROR_CODES and 'exc_info' in kwargs:
            exc_info = kwargs.pop('exc_info')
            self.write({'error_message': exc_info[1].log_message})
            self.finish()
        else:
            super(AddMetricsHandler, self).write_error(status_code, **kwargs)

api_urls = [
    (r'^/api/metrics/(.*)/(.*)/(.*)$', AddMetricsHandler),
    (r'^/api/metrics/(.*)/(.*)$', AddMetricsHandler),
]
