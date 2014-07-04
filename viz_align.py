#!/usr/bin/env python

'''Text-only Alignment Visualization tool
By Liang Huang (lhuang3@cis.upenn.edu, lhuang@isi.edu)

See below or simple type "viz_align.py" to see the usage.
'''

import sys
#sys.path.append("~/newcode")

import time
import copy
import math
import phraseO

from align_tool import *

logs = sys.stderr

def usage():
	print >> logs, "Text-only Alignment Vizualization Tool \nUsage: "
	print >> logs, "viz_align.py [options] <e-corpus> <f-corpus> <alignment1> [<alignment2>]"
	print >> logs, " options:"
	print >> logs, " \t" + "%-25s" % "-i, --inv" + "inverse alignment (default: e-f)"
	print >> logs, " \t" + "%-25s" % "-b, --batch" + "batch mode (for printing)"	
	print >> logs, " \t" + "%-25s" % "-f NUM, --first NUM" + "only the first NUM sentence pairs"	
	print >> logs, " \t" + "%-25s" % "-m LEN" + "no more than LEN words on the English side"	
	print >> logs, " \t" + "%-25s" % "-d, --diff" + "only show sentence pairs with different alignments"
	print >> logs, " \t" + "%-25s" % "--GB" + "use GB encoding (default: UTF-8)"
	print >> logs, " \t" + "%-25s" % "-e, --euro" + "english with european languages"
	
	print >> logs, "\ne.g.:"
	print >> logs, "./viz_align.py --GB 10.e 10.f 10.union 10.grow"
	sys.exit(1)

pattern = ["- ", ". ", "--", "."]
coding = 3  # default : UTF

def tag(e, c, alignment, another):
	aa = (e, c) in alignment
	bb = (e, c) in another
	if aa and bb:
		return "%d" % (c)
	if not aa and not bb:
		return pattern[e % 4]
	if aa:
		return "<" + str(c)
	else:
		return ">" + str(c)

def show(etext, ftext, alignment, another=None):

	if not another:
		another = alignment
	
	ewidth = max (map(len, etext)) + 3
	fheight = max (map(len, ftext))
	fwidth = 4
	eformat = "%%2d %%%ds" % (ewidth-3)
	fformat = "%%-%ds" % (fwidth-1) 
	vertical = "%%%ds" % fheight

	cooked_f = []
	for f in ftext:
		cooked_f.append(vertical % f)

	#chinese
	for i in range(int(math.ceil( float(fheight) / coding))):
		print " " * ewidth,
		for f in cooked_f:
			if f[i*coding] == " ":
				print fformat % f[i*coding:(i+1)*coding],
			else:
				print fformat % f[i*coding:(i+1)*coding] + " "*(coding-2), 
		print
		
	#print " " * ewidth, "-" * len(ftext) * fwidth

	#numbers
	print " " * ewidth,
	for c in range(len(ftext)):
		print fformat % c,
	print
	print
	
	for e, ew in enumerate(etext):
		print eformat % (e, ew), 
		for c in range(len(ftext)):
			print fformat % tag(e, c, alignment, another),
		print "%-10s %d" % (ew, e)
		
	
if __name__ == "__main__":

	only_diff = False
	inverse = False
	batch = False
	first = None
	cutoff = None
	phrase = False
	import getopt
	try:
		opts, args = getopt.getopt(sys.argv[1:], "dibf:m:e",\
								   ["diff", "GB", "inv", "batch", "first=", "euro", "p"])
	except:
		usage()
	for o, a in opts:
		if o in ["-d", "--diff"]:
			only_diff = True
		elif o in ["--GB"]:
			coding = 2
		elif o in ["-i", "--inv"]:
			inverse = True
		elif o in ["-b", "--batch"]:
			batch = True
		elif o in ["-f", "--first"]:
			first = int(a)
		elif o in ["-m"]:
			cutoff = int(a)
		elif o in ["-e", "--euro"]:
			coding = 2
		elif o in ["--p"]:
			phrase = True
		else:
			usage()

	if len(args) not in [3, 4]:
		usage()

	efile, ffile, alignfile = map(open, args[:3])
	comparefile = None
	if len(args) > 3:
		comparefile = open(args[3])
	elif only_diff:
		usage()  # can't compare if there is only one alignment

	goto = None
	for i, line in enumerate(alignfile):
		etext, ftext = efile.readline().split(), ffile.readline().split()
		alignment = get_alignment(line, i, len(etext), len(ftext), inverse)
		if comparefile:
			compareline = comparefile.readline()
			another = get_alignment(compareline, i, len(etext), len(ftext), inverse)
		else:
			another = None

		if phrase:
			print "#", i
			rectlist = phraseO.printAlignment(alignment)
			for r in rectlist:
				alignlist = r.alignlist
				list1 = []
				list2 = []
				for pos in alignlist:
					list1 = list1 + [pos[0]]
					list2 = list2 + [pos[1]]
				l1 = ""
				l2 = ""
				prev = ""
				for p in list1:
					if p == prev:
						continue
					l1 = l1 + etext[p] + " "
				prev = ""
				for p in list2:
					if prev == p:
						continue
					l2 = l2 + ftext[p] + " "
				print l1
				print l2



			continue;
		if goto is not None:
			if i + 1 < goto:
				continue
			else:
				goto = None

		
		if not another or not only_diff or alignment != another:
			show(etext, ftext, alignment, another)	

		if cutoff is not None and len(etext) > cutoff:
			continue
		
		print "sentence %d:" % (i+1),
		if another:
			a_b = alignment - another
			b_a = another - alignment

			if not a_b and not b_a:
				print "A == B  ",
			elif not a_b and b_a:
				print "A <= B  ",
			elif not b_a and a_b:
				print "A >= B  ",
			else:
				print "A <> B  ",
			if a_b:
				print " A-B =", len(a_b), ":", list(a_b), 
			if b_a:
				print " B-A =", len(b_a), ":",  list(b_a),

		if batch:
			print
		else:
			s = raw_input().strip()
			if s == "q":
				break
			else:
				try:
					goto = int(s)
				except:
					pass

		if first is not None and i + 1 >= first:
			break
				
	
