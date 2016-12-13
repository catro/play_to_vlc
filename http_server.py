#!/bin/python
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import os
import mutex
import thread
import urllib2
from datetime import timedelta
from datetime import datetime

PORT = 8000

class Douyu(object):
    
    @staticmethod
    def get_encoded_url(url):
        return 'http://localhost:' + str(PORT) + '/douyu/' + url

    def __init__(self):
        self.response = None
        self.info = None

    def connect(self, url):
        try:
            self.response = urllib2.urlopen(urllib2.Request(url, headers={'User-Agent': 'kodi'}))
            self.info = self.response.info()
            return True
        except:
            self.response = None
            self.info = None
            print('[Douyu]Connect fail')
            return False

    def send_header(self, request_handler):
        if (self.info is None):
            print('[Douyu]send_header fail')
            request_handler.send_error(404)
            return False

        request_handler.send_response(200)
        for item in self.info:
            request_handler.send_header(item[0], item[1])
        request_handler.end_headers()
        return True
        
    def do_HEAD(self, request_handler):
        print('[Douyu]do_HEAD')
        self.send_header(request_handler)

    def do_GET(self, request_handler):
        print('[Douyu]do_GET')
        if (self.send_header(request_handler) is False):
            return

        try:
            while True:
                request_handler.wfile.write(self.response.read())
        except:
            print('[Douyu]do_GET fail')
            self.response.close()
    

def process_url(url):
    #os.system('you-get -p "vlc -f --http-port=8081" "' + url + '"')
    #os.system('you-get -p "python play_to_kodi.py" "' + url + '"')
    os.system('you-get -p "python test.py" "' + url + '"')

douyu = None

class http_server(SimpleHTTPRequestHandler):
    def do_GET(self):
        if (self.path[1:5] == 'http'):
            url = self.path[1:].replace('/m.', '/www.')
            print "Got GET request %s" % (url)
            thread.start_new_thread(process_url, (url,))
            try:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("<html><head><script>void(function back(){window.close()})()</script></head><body /></html>")
            except:
                pass
        elif (self.path[1:6] == 'douyu'):
            global douyu
            douyu = Douyu()
            if (douyu.connect(self.path[7:])):
            #if (douyu):
                douyu.do_GET(self)
                del douyu

    def do_HEAD(self):
        if (self.path[1:6] == 'douyu'):
            global douyu
            douyu = Douyu()
            if (douyu.connect(self.path[7:])):
                douyu.do_HEAD(self)
            else:
                del douyu


if __name__ == "__main__":
    httpd = SocketServer.TCPServer(("", PORT), http_server)
    httpd.serve_forever()

