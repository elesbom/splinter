#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import warnings
import tornado.ioloop
import tornado.httpserver
import tornado.web
from StringIO import StringIO
from urllib import urlopen
from multiprocessing import Process
warnings.simplefilter('ignore')

EXAMPLE_APP = "http://localhost:5000/"

EXAMPLE_HTML = '''
<html>
  <head>
    <title>Example Title</title>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
  </head>
  <body>
    <h1 id="firstheader">Example Header</h1>
    <h1 id="firstheader">Example Last Header</h1>
    <form action="name" method="GET">
        <label for="query">Query</label>
        <input type="text" name="query" value="default value" />
        <input type="text" name="query" value="default last value" />
        <label for="send">Send</label>
        <input type="submit" name="send" />
        <input type="radio" name="some-radio" value="choice" />
        <input type="radio" name="other-radio" value="other-choice" />
        <input type="checkbox" name="some-check" value="choice" />
        <input type="checkbox" name="checked-checkbox" value="choosed" checked="checked" />
        <select name="uf">
            <option value="mt">Mato Grosso</option>
            <option value="rj">Rio de Janeiro</option>
        </select>
    </form>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" name="upload" />
    </form>
    <a href="http://example.com">Link for Example.com</a>
    <a href="http://example.com/last">Link for Example.com</a>
    <a href="http://example.com">Link for last Example.com</a>
    <div id="visible">visible</div>
    <div id="invisible" style="display:none">invisible</div>
    <a href="/foo">FOO</a>
  </body>
</html>'''.strip()

class ExampleHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(EXAMPLE_HTML)

class NameHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('My name is: Master Splinter')

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.request.files['file']
        buf = [
            u'Content-type: %(content_type)s' % data,
            u'File content: %(body)s' % data,
        ]
        self.write(u"|".join(buf))

class FooHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('BAR!')

class MockServer(object):
    def start(self):
        default_port = 5000
        application = tornado.web.Application([
            (r"/", ExampleHandler),
            (r"/name", NameHandler),
            (r"/upload", UploadHandler),
            (r"/foo", FooHandler),
        ])
        def go(app, port):
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            warnings.simplefilter('ignore')
            http = tornado.httpserver.HTTPServer(app)
            http.listen(int(port))
            tornado.ioloop.IOLoop.instance().start()

        process = Process(target=go, args=[application, default_port])
        process.start()
        for timeout in range(120):
            try:
                urlopen(EXAMPLE_APP)
                break
            except IOError:
                time.sleep(0.1)

        assert timeout != 119, \
            u"couldn't start splinter's http server on localhost:%d" % default_port

        self.process = process

    def stop(self):
        try:
            os.kill(self.process.pid, 9)
        except OSError:
            self.process.terminate()
