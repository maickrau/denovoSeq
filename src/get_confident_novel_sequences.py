#!/usr/bin/python

import sys

node_color_csv = sys.argv[1]
# gfa from stdin
# nodes to stdout

def revnode(n):
	return (">" if n[0] == "<" else "<") + n[1:]

def getone(s):
	for c in s: return c

def check_valid_bubble(edges, node_colors, node):
	if node not in edges: return False
	if revnode(node) not in edges: return False
	if len(edges[node]) != 1: return False
	if len(edges[revnode(node)]) != 1: return False
	prenode = revnode(getone(edges[revnode(node)]))
	postnode = getone(edges[node])
	if len(edges[prenode]) != 2: return False
	if len(edges[revnode(postnode)]) != 2: return False
	altnode = None
	for n in edges[prenode]:
		if n != node:
			assert altnode is None
			altnode = n
	assert altnode is not None
	if len(edges[revnode(altnode)]) != 1: return False
	if altnode not in edges: return False
	if len(edges[altnode]) != 1: return False
	if getone(edges[altnode]) != postnode: return False
	if "hap1" in node_colors[altnode[1:]]: return False
	if len(node_colors[altnode[1:]]) != len(node_colors[prenode[1:]]) - 1: return False
	if len(node_colors[altnode[1:]]) != len(node_colors[postnode[1:]]) - 1: return False
	if "hap1" not in node_colors[prenode[1:]]: return False
	if "hap1" not in node_colors[postnode[1:]]: return False
	mid_nodes = set()
	for hap in node_colors[node[1:]]: mid_nodes.add(hap)
	for hap in node_colors[altnode[1:]]: mid_nodes.add(hap)
	if mid_nodes != node_colors[prenode[1:]]: return False
	if mid_nodes != node_colors[postnode[1:]]: return False
	return True

node_colors = {}
with open(node_color_csv) as f:
	for l in f:
		parts = l.strip().split(',')
		node = parts[0]
		haps = set(parts[1].split(':'))
		node_colors[node] = haps

edges = {}
for l in sys.stdin:
	parts = l.strip().split('\t')
	if parts[0] == "L":
		fromnode = (">" if parts[2] == "+" else "<") + parts[1]
		tonode = (">" if parts[4] == "+" else "<") + parts[3]
		if fromnode not in edges: edges[fromnode] = set()
		edges[fromnode].add(tonode)
		if revnode(tonode) not in edges: edges[revnode(tonode)] = set()
		edges[revnode(tonode)].add(revnode(fromnode))

for node in node_colors:
	assert node in node_colors
	if len(node_colors[node]) != 1 or getone(node_colors[node]) != "hap1": continue
	if not check_valid_bubble(edges, node_colors, ">" + node): continue
	print(node)
