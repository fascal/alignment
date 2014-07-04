#!/usr/bin/env python

import sys
last = None
for line in sys.stdin:
	sid, a, b = map(int, line.split())
	if sid != last:
		if last is not None:
			print
		last = sid
	print "%d-%d" % (a-1, b-1),

