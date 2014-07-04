#!/usr/bin/env python

import sys, os
#sys.path.append(os.environ["NEWCODE"])

import time
import copy
#from myutils import *

logs = sys.stderr

def usage():
	print >> logs, "cat align-union | ~/newcode/alignment.py [-u|-i] [-g gm] [-f fm] [--diagfirst] [--inv] [--sort-by-e] [--no-t-shape]"
	print >> logs, "\t--inv     : inverted input (for david)"
	print >> logs, "\t--second  : sorting using the second field (for comparison with HPC data)"
	print >> logs, "\tu         : union (not just concatenation!)"
	print >> logs, "\ti         : intersection"
	print >> logs, "\tg method  : grow_diag. method = and/or"	
	print >> logs, "\tf method  : final. method = and/or"	
	print >> logs, "note:  u|i|g"
	print >> logs, "e.g.:"
	print >> logs, "\t -g or -f and means grow_diag_final_and, the default for pharaoh"
	sys.exit(1)

moves = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

def swap((a,b)):
        return (b,a)

inverse = False
criteria = swap

def set_inverse(inv):
	global inverse
	inverse = inv

def getopts():
	global heuristic, inverse, elenfile, flenfile
	global use_grow, use_diag, use_final, final_and, use_union, use_intersection
	use_grow, use_diag, use_final, final_and, use_union, use_intersection, inverse = (False, ) * 7

	global criteria, moves, allow_tshape

	allow_tshape = True

	import getopt

	try:
		opts, args = getopt.getopt(sys.argv[1:], "uigdfa", ["inv", "sort-by-e", "diagfirst", "no-t-shape"])
	except:
		usage()
	for o, a in opts:
		if o == "-u":
			use_union = True
		elif o == "-i":
			use_intersection = True		
		elif o == "-g":
			use_grow = True
		elif o == "-d":
			use_diag = True
		elif o == "-f":
			use_final = True		
		elif o == "-a":
			final_and = True
		elif o == "--diagfirst":
			moves = moves[4:] + moves[:4]
		elif o == "--inv":
			inverse = True		
		elif o == "--sort-by-e":
			criteria = None
		elif o == "--no-t-shape":
			allow_tshape = False
		else:
			usage()

	if (use_diag and not use_grow) or (final_and and not use_final) \
		   or (int(use_union) + int(use_intersection) + int(use_grow) != 1):
		usage()

	if not use_diag:
		moves = moves[:]

	if len(args) == 2:
		elenfile, flenfile = open(args[0]), open(args[1])							  
	else:
		elenfile, flenfile = None, None
		
def getpairint(pair):
  x, y = pair.split("-")[:2]  # optional prob like 0-1-0.999
  if inverse:
    x, y = y, x
  return int(x), int(y)

def outrange(p, limit):
	return p < 0 or p >= limit

def tshape(e, c, alignment):
	if (e, c) in alignment:
		horiz = (e + 1, c) in alignment  or  (e - 1, c) in alignment
		verti = (e, c + 1) in alignment  or  (e, c - 1) in alignment
		return horiz and verti
	return False

def thereistshape(e, c, alignment):
	alignment.add((e,c))
	result = tshape(e, c, alignment) \
			 or tshape(e + 1, c, alignment) or tshape(e - 1, c, alignment) \
			 or tshape(e, c + 1, alignment) or tshape(e, c - 1, alignment)
	alignment.discard((e,c))
	return result

def print_alignment(alignment, out=sys.stdout, giza=False, cr=criteria, pr=None):
	if giza:
		format = "%d %d"
	else:
		format = "%d-%d"
	for e, c in sorted(alignment, key=cr):
		if pr:
			e, c = pr((e, c))
		print >> out, format % (e, c) ,
	print >> out

def isneighbor(e, c, alignment):
	for emov, cmov in moves:
		enew, cnew = e + emov, c + cmov
		if (enew, cnew) in alignment:
			return True
	return False

def grow(alignment, union):

	print >> logs, "starting with intersection"
	print_alignment(alignment, logs)
	
	e_aligned = set([e for (e, _) in alignment])
	c_aligned = set([c for (_, c) in alignment])

	
	changed = True
	while changed:
		changed = False
		print >> logs, "iteration..."

		justfailed = set([])
		for e, c in sorted(alignment):
			for emov, cmov in moves:
				enew, cnew = e + emov, c + cmov
				if (enew, cnew) not in justfailed \
					   and (enew, cnew) not in alignment \
					   and (enew, cnew) in union \
					   and (enew not in e_aligned  or   cnew not in c_aligned) \
					   and isneighbor(enew, cnew, alignment) \
					   and (allow_tshape or not thereistshape(enew, cnew, alignment)):
					changed = True
					alignment.add((enew, cnew))
					e_aligned.add(enew)
					c_aligned.add(cnew)
					print >> logs, "adding %d-%d from %d-%d" % (enew, cnew, e, c),
				else:
					justfailed.add((enew, cnew))
	print >> logs

def final(alignment, union, final_and):
	print >> logs, "final"
	e_aligned = set([e for (e, _) in alignment])
	c_aligned = set([c for (_, c) in alignment])
	for e, c in union:
		if (e not in e_aligned) and (c not in c_aligned) \
			   and (allow_tshape or not thereistshape(e, c, alignment)):
			alignment.add((e,c))			
			e_aligned.add(e)
			c_aligned.add(c)
			print >> logs, "adding %d-%d" % (e, c),
	print >> logs
	
def get_two_alignments(line, i=-1, lene=None, lenf=None, inv=False):
	lastc = -1
	dir = 0
	points = set([]), set([])
	
	pairs = line.split()
	for pair in pairs:
		e, c = getpairint(pair)
		if inv:
			e, c = c, e
		if lene and (outrange(e, lene) or outrange(c, lenf)):
			print >> logs, "line %d: alignment points (%d, %d) out of range [0, %d) x [0, %d)" \
				  % (i+1, e, c, lene, lenf)
			
		if dir == 0 and c < lastc:
			dir = 1
		points [dir].add((e, c))
		lastc = c
	return points

def get_alignment(line, i=-1, lene=None, lenf=None, inv=False):
	points = set([])
	pairs = line.split()
	for pair in pairs:
		e, c = getpairint(pair)
		if inv:
			e, c = c, e
		if lene and (outrange(e, lene) or outrange(c, lenf)):
			print >> logs, "line %d: alignment points (%d, %d) out of range [0, %d) x [0, %d)" \
				  % (i+1, e, c, lene, lenf)

		points.add((e, c))
	return points

def intersect(a, b):
	return a & b

def union(a, b):
	return a | b

cuma = cums = cumas = cumap = 0
def init_counts():
	global cuma, cums, cumas, cumap
	cuma = cums = cumas = cumap = 0

def calc(ass, ap, la, ls):
	prec, recall = ap / la, ass / ls
	aer = 1 - ( (ass + ap) / (la + ls) )
	
	return map(lambda x:x*100.0, (prec, recall, aer))

def prec_recall_AER(a, s, p):
	global cuma, cums, cumas, cumap

	la, ls = len(a) + 0.00001, len(s) + 0.00001
	ass = float (len (a & s))
	ap = float (len (a & p))
	cuma += la
	cums += ls
	cumas += ass
	cumap += ap

	return calc(ass, ap, la, ls)

def cum_AER():
	x = calc(cumas, cumap, cuma, cums)
	init_counts()
	return x

def split_alignment(a, x, y):
	'''split the permutation at (x, y). if successful, return the split a = (re; rf) with true, i.e. (True, re, rf)
	otherwise False and re and rf will contain the crossing (bottom-left and top-right) points'''

	re = [(e, f) for (e, f) in a if e >= x and f < y]
	rf = [(e, f) for (e, f) in a if e < x and f >= y]

	if re != [] or rf != []:
		return False, re, rf
	re = set([(e, f) for (e, f) in a if e < x and f < y])
	rf = set([(e-x, f-y) for (e, f) in a if e >= x and f >= y]) # caution: moved!
	return True, re, rf	
	
def main():
	for i, line in enumerate(sys.stdin):   # don't zip: not lazy

		if (i+1) % 10000 == 0:
			print >> logs, i+1, "lines processed"

		lene, lenf = None, None
		if elenfile:			
			lene, lenf = int(elenfile.readline()), int(flenfile.readline())		
		
		points = get_two_alignments(line, i, lene, lenf)

		union = points[0] | points[1]
		
		if use_union:   # compacter than original input, which is just concatenation
			print_alignment(union)
			continue
			
		alignment = points[0] & points[1]  # intersection is the base of grow and final

		while True:
			clone = sorted(alignment)
			if use_grow: 
				grow(alignment, union)
				
			if use_final:
				final(alignment, union, final_and)
			
			if sorted(alignment) == clone:
				break			
			
		print_alignment(alignment)
		
		
if __name__ == "__main__":
	try:
		import psyco
		psyco.full()
	except:
		pass
	getopts()
	main()
