import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from paver.easy import task, cmdopts, sh
from paver.tasks import help

@task
@cmdopts([
    ('port=', 'p', 'port to bind the server, default 8000'),
    ('daemon', 'd', 'run server on background'),
])
def start(options):
    ''' Start server '''

    import stewie.config
    stewie.config.load_settings(os.environ.get('STEWIE_ENV', 'dev'))

    from stewie.server import Server
    server = Server(port=options.get('port', 8000))

    from stewie.lib import daemon
    
    if options.start.get('daemon'):
        daemon.daemonize('/tmp/stewie.pid')

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


@task
@cmdopts([
    ('keyword=', 'k', 'pass keyword to py.test'),
    ('noserver', 'n', 'do not start the test server'),
])
def test(options):
    ''' Run all tests '''
    import pytest
    import stewie.config
    stewie.config.load_settings(os.environ.get('STEWIE_ENV', 'test'))

    if not options.get('noserver'):
        _start_test_server()

    args = ['-vs', 'stewie/tests']

    keyword = options.get('keyword')
    if keyword:
        args.append('-k ' + keyword)

    ret = pytest.main(args)

    if not options.get('noserver'):
        _stop_test_server()

    exit(ret)

def _start_test_server():
    sh("rm -f tests/server.log")
    sh("STEWIE_ENV=test paver start -p7766 & ")
    time.sleep(.5)

def _stop_test_server():
    sh("ps ax | grep 'paver start -p7766' | grep -v grep | awk '{ print $1 }' | xargs kill")
    print "Server logs on tests/server.log"
