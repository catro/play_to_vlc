#!/bin/python
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import os
import mutex
import threading
from datetime import timedelta
from datetime import datetime

PORT = 8000

class http_server(SimpleHTTPRequestHandler):
    def do_GET(self):
        print "Got GET request %s" % (self.path[1:])
        if (self.path[1:5] == 'http'):
            url = self.path[1:].replace('/m.', '/www.')
            os.system('start you-get -p vlc "' + url + '"')
            #os.system('you-get -p "python play_to_kodi.py" "' + url + '"')
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><script>void(function back(){window.history.back()})()</script></head><body /></html>")

if __name__ == "__main__":
    httpd = SocketServer.TCPServer(("", PORT), http_server)
    httpd.serve_forever()

