import os.path
# import logging

from tornado import ioloop
from tornado.httpserver import HTTPServer
from tornado.web import Application

from stewie.handlers import urls
from stewie.config import settings
# from stewie.lib import log

class Server(object):

    def __init__(self, port):
        self.port = int(port)
        self.my_directory = os.path.abspath(os.path.dirname(__file__))
        self.static_path = os.path.join(self.my_directory, 'static')
        self.template_path = os.path.join(self.my_directory, 'templates')
    #     self.setup_log()
    # 
    # def setup_log(self):
    #     logconfig = {}
    #     if settings.DEBUG:
    #         logconfig['level'] = logging.DEBUG
    #     if settings.LOG_FILE:
    #         logconfig['filename'] = settings.LOG_FILE
    # 
    #     log.configure(**logconfig)

    def start(self):
        self._setup_application()
        self._start_http_server()
        self._start_ioloop()

    def stop(self):
        ioloop.IOLoop.instance().stop()

    def _setup_application(self):
        self.application = Application(urls, **{
                'debug': True,
                'cookie_secret': 'n34n$nan$mndln*nldnANN!Anmdlksn',
                'xsrf_cookies': False,
                'static_path': self.static_path,
                'template_path': self.template_path,
                })

    def _start_http_server(self):
        self.application.listen(self.port)

    def _start_ioloop(self):
        print "Listening on %s" % self.port
        ioloop.IOLoop.instance().start()

