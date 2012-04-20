
from tornado.web import RequestHandler

class AdminController(RequestHandler):
    def get(self):
        pass

admin_urls = [
    (r'/', AdminController),
]
