#!/usr/bin/env python

# interunion.py [-i|-u] etof.a ftoe.a > inter|union.a

import sys
from align_tool import *

if __name__ == "__main__":
	if len(sys.argv) != 4 or sys.argv[1] not in ["-i", "-u"]:
		print "usage:"
		print "\t./interunion.py [-i|-u] etof.a ftoe.a > output"
		exit
	else:
		inter = sys.argv[1] == "-i"
		
	etof, ftoe = map(open, sys.argv[2:4])

	for i, (linea, lineb) in enumerate(zip(etof, ftoe)):
		aa, bb = map(get_alignment, (linea, lineb))
		cc = intersect(aa, bb) if inter else union(aa, bb)
		print_alignment(cc)

