#!/usr/bin/env python

# AER.py [-d] <test.a> <gold-s.a> [<gold-p.a>]"

import sys
from align_tool import *

if __name__ == "__main__":
	details = False
	if sys.argv[1] == "-d":
		details = True
		del sys.argv[1]
		
	files = map(open, sys.argv[1:])
	if len(sys.argv) == 4:
		fa, fs, fp = files
	else:
		fa, fs = files
		fp = open(sys.argv[-1])
	
	for i, (a, s, p) in enumerate(zip(fa, fs, fp)):
		aa = get_alignment(a)
		ss = get_alignment(s)
		pp = get_alignment(p)

		prec, recall, AER = prec_recall_AER(aa, ss, pp)

		if details:
			print "sentence %d\tprecision = %5.2lf\trecall = %5.2lf\t\tAER = %5.2lf" % (i+1, prec, recall, AER)

	
	prec, recall, AER = cum_AER()
	if details:
		print
	print "total %d\tprecision = %5.2lf\trecall = %5.2lf\t\tAER = %5.2lf" % (i+1, prec, recall, AER)
