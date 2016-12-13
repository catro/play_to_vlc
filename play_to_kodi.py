#!/bin/python
import sys
import requests
import json
from urllib import quote_plus
from http_server import Douyu

def send_jsonrpc(method, parameters, port):
    url = "http://localhost:" + str(port) + "/jsonrpc?request="
    rpc = {"jsonrpc": "2.0",
            "method": method,
            "id": 1}
    if parameters:
        rpc["params"] = parameters

    url += quote_plus(json.dumps(rpc))
    r = requests.get(url)
    print r.content


def play_to_kodi(urls, port = 8080):
    parameters = {"playlistid": 1}
    send_jsonrpc("Playlist.Clear", parameters, port)

    parameters = {"playlistid": 1}
    playlist = []
    if ((len(urls) == 1) and 
            ('douyu' in urls[0])):
        playlist.append({"file": Douyu.get_encoded_url(urls[0])})
    else:
        for url in urls:
            playlist.append({"file": url})
    parameters["item"] = playlist
    send_jsonrpc("Playlist.Add", parameters, port)

    parameters = {"item": {"playlistid": 1}}
    send_jsonrpc("Player.Open", parameters, port)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        play_to_kodi(sys.argv[1:])
