#!/bin/sh

set -e

help(){
    echo "see segments.csv file for available segments"
}

[ "$1" = "-h" ] || [ "$1" = "--help" ] && help && exit 0

[ -n "$2" ] && [ "$2" -gt 2020 ] && echo "year can be max 2020" && exit 1
[ -n "$2" ] && [ "$2" -lt 2007 ] && echo "year have to be at least 2007" && exit 1

RAND_SEG="$(shuf -n 1 < segments.csv)"
Y="$(echo "$RAND_SEG" | cut -d ',' -f1)"
DD="$(echo "$RAND_SEG" | cut -d ',' -f2)"
MAX_PATHS="10"

[ -n "$1" ] && MAX_PATHS="$1"
[ -n "$2" ] && Y="$2"
[ -n "$3" ] && DD="$3"

curl -f "https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-$Y-$DD/warc.paths.gz" | gzip -d | shuf -n "$MAX_PATHS" | while read url; do
    echo "https://commoncrawl.s3.amazonaws.com/$url"
done
