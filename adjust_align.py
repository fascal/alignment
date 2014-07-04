#!/usr/bin/env python

'''adjust alignment by comparing two word segmentations'''

# adjust_align.py dev.a dev.f dev.f.seg [dev.E] > dev.a.seg

import sys
from align_tool import *

logs = sys.stderr

if __name__ == "__main__":
	afile, oldfile, newfile = map(open, sys.argv[1:4])
	efile = open(sys.argv[4]) if len(sys.argv) > 4 else None

	for i, (aline, oldline, newline) in enumerate(zip(afile, oldfile, newfile)):
		eline = efile.readline().split() if efile is not None else None

		al = get_alignment(aline)

		oldline, newline = map(lambda x:x.split(), (oldline, newline))
		oldlen, newlen = map(len, (oldline, newline))

		j = k = 0

		while j < oldlen and k < newlen:
			oldword = oldline[j]
			newword = newline[k]

			if len(oldword) == len(newword):
				assert oldword == newword, "BAD segmentation at #%d: %s != %s" % (i+1, oldword, newword)

				print " ".join(["%d-%d" % (e, f + (k-j)) for (e, f) in al if f == j ]),

			elif len(oldword) < len(newword):
				# jj+1j+2
				# o o o
				# nnnnn
				# k
				startj = j				
				while j < oldlen:
					print " ".join(["%d-%d" % (e, f + (k-j)) for (e, f) in al if f == j  ]),
					print >> logs, oldline[j],
					if eline:
						print >> logs, ":{", " ".join([eline[l] for (l, y) in al if y==j]), "}",
					if len(oldword) >= len(newword):
						break
					j += 1
					oldword += oldline[j]

				print >> logs, "=>", newword

				assert oldword == newword, "BAD segmentation at #%d: %s != %s" % (i+1, oldword, newword)
				
			else:
				# ooooo
				# n n n
				print >> logs, oldword,
				if eline:
					print >> logs, ":{", " ".join([eline[l] for (l, y) in al if y==j]), "} =>",
					
				startk = k
				while k < newlen:
					print " ".join(["%d-%d" % (e, f + (k-j)) for (e, f) in al if f == j ]),				
					print >> logs, newline[k],
					if len(oldword) <= len(newword):
						break
					k += 1
					newword += newline[k]

				print >> logs

				assert oldword == newword, "BAD segmentation at #%d: %s != %s" % (i+1, oldword, newword)

			j += 1
			k += 1

		assert j == oldlen and k == newlen, "BAD segmentation at #%d"
		print 

		
