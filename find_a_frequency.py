#!/usr/bin/python3
from collections import Counter
from bs4 import BeautifulSoup
import sys
import requests
from warcio.archiveiterator import ArchiveIterator

dict = {'a':0,'rest':0}
max_records = 1000
source_index = 1

if len(sys.argv) > 1:
    max_records = int(sys.argv[1])

def print_records(url, source):
    hit = 1
    resp = requests.get(url, stream=True)

    for record in ArchiveIterator(resp.raw, arc2warc=True):
        if record.rec_type != 'warcinfo':
            if hit <= max_records:
                if record.rec_type == 'response':
                    if record.http_headers.get_header('Content-Type') == 'text/html':
                        raw = record.content_stream().read()
                        cleantext = BeautifulSoup(raw, "lxml").text
                        for c in cleantext:
                            if c == 'a':
                                dict['a'] += 1
                            else:
                                dict['rest'] +=1

                        print("\rsource(" + str(source) + ") hit(" + str(hit) + ") {:.6f}%".format(dict['a'] / dict['rest'] * 100), end="")
                        hit += 1
            else:
                print("\nsource record limit reached.")
                break

print("a frequency in given website records:")
try:
    for url in map(str.rstrip, sys.stdin):
        print_records(url, source_index)
        source_index += 1

except KeyboardInterrupt:
    print('\nInterrupted')
    sys.exit(0)
