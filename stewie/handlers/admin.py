
from tornado.web import RequestHandler

from stewie import models

class AdminController(RequestHandler):
    def get(self):
        self.render('index.html', events=models.find_anomalous_events())

admin_urls = [
    (r'/', AdminController),
]
