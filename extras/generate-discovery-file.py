#!/usr/bin/python

from dse.cluster import Cluster
import sys
import json
import shutil

argv_len = len(sys.argv)
if (argv_len < 3 or sys.argv[1] == '--help' or sys.argv[1] == '-h'):
    print("Usage: generate.py contact_point file_name [port]")
    exit(1)

port = '9103'
if (argv_len == 4):
    port = sys.argv[3]

cluster = Cluster([sys.argv[1]])
session = cluster.connect()
metadata = cluster.metadata

host_list = [host.broadcast_address + ':' + port for host in metadata.all_hosts()]

data = {'labels': {'cluster': metadata.cluster_name}, 'targets': host_list}
filename = sys.argv[2] + '.tmp'
with open(filename, 'w') as f:
    json.dump(data, f)

shutil.move(filename, sys.argv[2])
