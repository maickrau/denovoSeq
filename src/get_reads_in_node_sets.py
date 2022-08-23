#!/usr/bin/python

import sys

node_list_in = sys.argv[1]
# gaf from stdin
# info to stdout

case_reads_list = {}
with open(node_list_in) as f:
	for l in f:
		case_reads_list[l.strip()] = set()

for l in sys.stdin:
	parts = l.strip().split('\t')
	readname = parts[0]
	path = parts[5].replace('>', '\t').replace('<', '\t').strip().split('\t')
	for node in path:
		if node in case_reads_list:
			case_reads_list[node].add(readname)

for node in case_reads_list:
	print("MBG node ID " + node)
	print("reads:")
	for read in case_reads_list[node]:
		print(read)
	print("")
