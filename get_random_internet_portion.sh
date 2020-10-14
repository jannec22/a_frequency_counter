#!/bin/sh

set -e

help(){
    echo "see segments.csv file for available segments"
}

[ "$1" = "-h" ] || [ "$1" = "--help" ] && help && exit 0

[ -n "$2" ] && ! cat segments.csv | cut -d ',' -f1 | grep -q >/dev/null >&2 "$2" && echo "year have to be in a list of segments (check segments.csv)">&2 && exit 1
[ -n "$3" ] && ! cat segments.csv | cut -d ',' -f2 | grep -q >/dev/null >&2 "$3" && echo "day have to be in a list of segments (check segments.csv)">&2 && exit 1

MAX_PATHS="10"

[ -n "$1" ] && MAX_PATHS="$1"
[ -n "$2" ] && Y="$2"
[ -n "$3" ] && DD="$3"

RAND_SEG="$(shuf -n 1 < segments.csv)"
[ -z "$Y" ] && Y="$(echo "$RAND_SEG" | cut -d ',' -f1)"
[ -z "$Y" ] && DD="$(echo "$RAND_SEG" | cut -d ',' -f2)"
[ -z "$DD" ] && DD="$(cat segments.csv | cut -d ',' -f1,2 | grep "$Y," | cut -d ',' -f2 | shuf -n 1)"

curl -fs "https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-$Y-$DD/warc.paths.gz" | gzip -d | shuf -n "$MAX_PATHS" | while read url; do
    echo "https://commoncrawl.s3.amazonaws.com/$url"
done
