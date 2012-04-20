import os.path

ENV = 'test'

DB_HOST = 'localhost'
DB_NAME = 'stewie'

here = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(here, '..', 'tests', 'server.log')
