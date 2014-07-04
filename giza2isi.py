#!/usr/bin/env python

'''convert GIZA alignments into ISI format (0-0 1-1..)'''


# NULL ({ 1 4 5 6 7 8 9 }) the ({ 3 }) commissionners ({ 2 }) went ({ 10 }) on ({  }) : ({ 11 })
# =>
# 0-2 1-1 3-9 5-10 ...

import sys, os, re
sys.path.append(os.environ["NEWCODE"])

logs = sys.stderr

pattern = re.compile(r'\S+ \(\{ (.*?) \}\)')

def giza2isi(line):
	align = pattern.findall(line)
	s = []
	for e, nums in enumerate(align[1:]):   # skip NULL
		fs = map(int, nums.split())
		for f in fs:
			s.append((e,f-1) if not inv else (f-1,e))
	return " ".join(["%d-%d" % e_f for e_f in s])

if __name__ == "__main__":
	inv = "-i" in sys.argv		
	for line in sys.stdin:
		line = line.strip()
		if line[0:4] == "NULL":
			print giza2isi(line)
			
			
