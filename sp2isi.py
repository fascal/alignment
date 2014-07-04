#!/usr/bin/env python

# convert Sure/Possible format into 0-0 1-1 for S/P, respectively

# 1001 1 1 S
# 1001 2 2 P

# sure (-S):
# 0-0

# possible (-PS):
# 0-0 1-1

# possible - sure (-P):
# 1-1

import sys
last = None

try:
	opt = sys.argv[1][1:]
except:
	opt = "-S"

for line in sys.stdin:
	line = line.split()
	sp = line[3]
	sid, a, b = map(int, line[:3])
	if sid != last:
		if last is not None:
			ll = int(last)
			ss = int(sid)
			for i in xrange(ss-ll):
				print
		last = sid
	if sp in opt:
		print "%d-%d" % (a-1, b-1),

