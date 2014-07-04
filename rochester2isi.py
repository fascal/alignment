#!/usr/bin/env python

'''convert rochester alignment format into ISI format. (by Liang Huang)
begin 1
1 1
end
===>
0-0
'''

import sys

for line in sys.stdin:
    line = line.strip()
    if line == "end":
        print
    else:
        e, f = line.split()
        if e != "begin":
            print "%d-%d" % (int(e)-1, int(f)-1),
