#!/usr/bin/python

import sys

hap_reads_files = sys.argv[1:] # order: child, mat, pat
# gaf from stdin
# csv to stdout

def get_color(haps):
	hapslist = list(haps)
	hapslist.sort()
	hapslist = ":".join(hapslist)
	if hapslist == "hap1":
		return "#00FF00"
	elif hapslist == "hap1:hap2":
		return "#FFAA88"
	elif hapslist == "hap2":
		return "#FFAAAA"
	elif hapslist == "hap3":
		return "#AAAAFF"
	elif hapslist == "hap1:hap3":
		return "#88AAFF"
	elif hapslist == "hap1:hap2:hap3":
		return "#99AA99"
	elif hapslist == "hap2:hap3":
		return "#AA88AA"
	assert False

read_hap = {}
for i in range(1, len(sys.argv)):
	with open(sys.argv[i]) as f:
		for l in f:
			read_hap[l.strip()] = "hap" + str(i)

node_haps = {}
for l in sys.stdin:
	parts = l.strip().split('\t')
	readname = parts[0]
	if readname not in read_hap: print(readname)
	assert readname in read_hap
	nodes = parts[5].replace('>', '\t').replace('<', '\t').strip().split('\t')
	for node in nodes:
		if node not in node_haps: node_haps[node] = set()
		node_haps[node].add(read_hap[readname])

print("node,haps,color")
for node in node_haps:
	haps = list(node_haps[node])
	haps.sort()
	print(node + "," + ":".join(haps) + "," + get_color(node_haps[node]))

