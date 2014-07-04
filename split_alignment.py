#!/usr/bin/env python
 
import sys
import time
from alignment import *

logs = sys.stderr

def usage():
	print >> logs, "cat align-union | ~/newcode/split_alignment.py [--GIZA] [--inv] file1 file2"
	print >> logs, "\t-G, --GIZA\t use GIZA format: 4 5 instead of 4-5"
	sys.exit(1)

giza = False

def getopts():
	global giza, norm_file, invr_file
	import getopt
	try:
		opts, args = getopt.getopt(sys.argv[1:], "G", ["GIZA", "inv"])
	except:
		usage()
	for o, a in opts:
		if o == "--GIZA":
			giza = True
		elif o == "--inv":
			set_inverse(True)
		else:
			usage()

	if len(args) == 2:
		norm_file, invr_file = open(args[0], "w"), open(args[1], "w")
	else:
		usage()
		
def main():
	for i, line in enumerate(sys.stdin):   # don't zip: not lazy

		if (i+1) % 10000 == 0:
			print >> logs, i+1, "lines processed"

		points = get_two_alignments(line, i)

		print_alignment(points[0], norm_file, giza, cr=None, pr=None)
		print_alignment(points[1], invr_file, giza, cr=swap, pr=None)		
		
if __name__ == "__main__":
	try:
		import psyco
		psyco.full()
	except:
		pass
	getopts()
	main()
