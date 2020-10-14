#!/usr/bin/python3
from bs4 import BeautifulSoup
import sys
import requests
from warcio.archiveiterator import ArchiveIterator

letter = 'a'
if len(sys.argv) > 1:
    letter = sys.argv[1]

dict = {'rest':0}
dict[letter] = 0
max_records = 1000
source_index = 1

if len(sys.argv) > 2:
    max_records = int(sys.argv[2])

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
                            if c == letter:
                                dict[letter] += 1
                            elif c.isalpha(): # count only a-zA-Z
                                dict['rest'] +=1

                        if dict['rest'] > 0:
                            print("\rsource(" + str(source) + ") hit(" + str(hit) + ") \"" + letter + "\" frequency: " + "{:.6f}%".format(dict[letter] / dict['rest'] * 100), end="")
                            hit += 1
            else:
                print("\r----------source record limit reached.----------")
                break

print("a frequency in given website records:")
try:
    for url in map(str.rstrip, sys.stdin):
        print_records(url, source_index)
        source_index += 1

except KeyboardInterrupt:
    print('\nInterrupted')
    sys.exit(0)

print("final \"" + letter + "\" frequency: " + "{:.6f}%".format(dict[letter] / dict['rest'] * 100))