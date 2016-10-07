#!/bin/python
import sys
import requests
import json
from urllib import quote_plus

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
    for url in urls:
        playlist.append({"file": url})
    parameters["item"] = playlist
    send_jsonrpc("Playlist.Add", parameters, port)

    parameters = {"item": {"playlistid": 1}}
    send_jsonrpc("Player.Open", parameters, port)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        play_to_kodi(sys.argv[1:])
