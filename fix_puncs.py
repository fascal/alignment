#!/usr/bin/env python

# fix closing puncs (,;:'>>) in the beginning of a chinese sentence

import sys

logs = sys.stderr

bad_puncs = set([",", ".", ";", ":", "?", "!", ")", "]", "}", ">"])

puncsfile = "/home/lhuang3/newcode/alignment/puncs.txt"

if __name__ == "__main__":

	for x in open(puncsfile):
		bad_puncs.add(x.split()[0])
	
	fixed = 0

	for i, line in enumerate(sys.stdin):
		line = line.split()
		
		good = 0
		if line[0] in bad_puncs:
			if i==0:
				print >> logs,  "WARNING: first sentence starts with a closing punc."

			fixed += 1
			for good in xrange(len(line)):
				if line[good] not in bad_puncs:
					break		
			
		if i>0:
			print " ".join(line[:good])         # for previous sentence
			if good > 0:
				print >> logs, "%d\t%s" % (i, " ".join(line[:good]))
			
		print " ".join(line[good:]),
		
	print

	print >> logs, "total lines = %d\tfixed = %d" % (i, fixed)
		
		
