#!/bin/bash
#
# File: generate.sh
#
# Created: Thursday, January  3 2019
#

if [ $# -lt 1 -o "$1" = "-h" ]; then
    echo "Usage: generate.sh filename [port]"
    exit 1
fi

FILE=$1
PORT=9103
if [ $# -eq 2 ]; then
    PORT=$2
fi
TMPFILE=generate-$$.tmp

echo '[{"targets": [' > $TMPFILE
cnt=0
for node in `nodetool status|grep -e '^[UD][NLJM] '|sed -e 's|^[UD][NLJM] *\([^ ]*\) .*$|\1|'`; do
    if [ $cnt -gt 0 ]; then
        echo -n ", " >> $TMPFILE
    fi
    echo -n "\"$node:$PORT\"" >> $TMPFILE
    cnt=$((1 + cnt))
done

CLUSTER_NAME=`nodetool describecluster|grep 'Name:'|sed -e 's|^.*Name: \(.*\)$|\1|'`
echo "" >> $TMPFILE
echo "],\"labels\": {\"cluster\": \"$CLUSTER_NAME\"}}]" >> $TMPFILE
mv $TMPFILE $FILE
