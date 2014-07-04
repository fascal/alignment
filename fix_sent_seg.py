#!/usr/bin/env python

# fix closing puncs (,;:'>>) in the beginning of a chinese sentence

import sys

logs = sys.stderr

e_puncs = set([",", ".", ";", ":", "?", "!", "\""])

puncsfile = "/home/lhuang3/newcode/alignment/puncs.txt"

c_puncs = set(e_puncs)			 

if __name__ == "__main__":

	for x in open(puncsfile):
		c_puncs.add(x.split()[0])

	efile = open(sys.argv[1])
	ffile = open(sys.argv[2])
	eout = open(sys.argv[1] + ".cor", "w")
	fout = open(sys.argv[2] + ".cor", "w")
	
	omitted = 0

	bad = False
	for i, (eline, fline) in enumerate(zip(efile, ffile)):
		elast, flast = map(lambda x: x.split()[-1], (eline, fline))		
		newbad = (elast in e_puncs) and (flast not in c_puncs)

		if bad or newbad:
			omitted += 1
			print >> logs, i, bad, newbad, eline,
			print >> logs, i, bad, newbad, fline,
			
		else:
			print >> eout, eline,
			print >> fout, fline,
			
		bad = newbad
		
	print >> logs, "total lines = %d\tomitted = %d" % (i, omitted)
		
		
