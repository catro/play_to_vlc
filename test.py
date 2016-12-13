#!/bin/python
import os
import sys
from http_server import Douyu

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = Douyu.get_encoded_url(sys.argv[1])
        print(url)
        os.system('vlc "' + url + '"')
