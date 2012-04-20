
from tornado.web import RequestHandler

from stewie import models
from stewie.detector import Detector

class AdminController(RequestHandler):
    def get(self):
        self.render('index.html', events=models.find_anomalous_events(), detector=Detector())

admin_urls = [
    (r'/', AdminController),
]
