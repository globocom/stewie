from tornado.web import RequestHandler, HTTPError

from stewie import models, detector

class AddMetricsHandler(RequestHandler):

    API_ERROR_CODES = 400,

    def post(self, bucket, target, timestamp=None):
        metrics = self.request.arguments
        try:
            models.add_event(bucket, target, metrics, timestamp)
        except models.ValidationError as ex:
            raise HTTPError(400, str(ex))

    def write_error(self, status_code, **kwargs):
        if status_code in self.API_ERROR_CODES and 'exc_info' in kwargs:
            exc_info = kwargs.pop('exc_info')
            self.write({'error_message': exc_info[1].log_message})
            self.finish()
        else:
            super(AddMetricsHandler, self).write_error(status_code, **kwargs)

    def raise_invalid_request(self):
        raise HTTPError(400)

api_urls = [
    (r'^/api/metrics/(.*)/(.*)/(.*)$', AddMetricsHandler),
    (r'^/api/metrics/(.*)/(.*)$', AddMetricsHandler),
]
