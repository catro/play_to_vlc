#!/bin/python
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import os
import mutex
import thread
from datetime import timedelta
from datetime import datetime

PORT = 8000

def process_url(url):
    os.system('you-get -p "vlc -f --http-port=8081" "' + url + '"')
    #os.system('you-get -p "python play_to_kodi.py" "' + url + '"')

class http_server(SimpleHTTPRequestHandler):
    def do_GET(self):
        if (self.path[1:5] == 'http'):
            url = self.path[1:].replace('/m.', '/www.')
            print "Got GET request %s" % (url)
            thread.start_new_thread(process_url, (url,))
            #os.system('start you-get -p vlc "' + url + '"')
            #os.system('you-get -p "python play_to_kodi.py" "' + url + '"')
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("<html><head><script>void(function back(){window.close()})()</script></head><body /></html>")
        except:
            pass

if __name__ == "__main__":
    httpd = SocketServer.TCPServer(("", PORT), http_server)
    httpd.serve_forever()

