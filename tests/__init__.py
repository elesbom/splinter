from splinter_server import MockServer

server = MockServer()
def setup():
    server.start()

def teardown():
    server.stop()
