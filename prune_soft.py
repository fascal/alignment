#!/usr/bin/env python

'''prune soft alignment matrix.
   input: e-f-prob ...
'''

import sys

if __name__ == "__main__":

  inv = False  # input is inverse (f-e) alignment? default: e-f
  threshold = 0.5 # default: 0.5
  hard = False # hard output
  
  for arg in sys.argv[1:]:
    if arg == "--inv":
      inv = True
    elif arg == "--hard":
      hard = True
    else:
      threshold = float(arg)  
  
  for line in sys.stdin:

    for point in line.split():
      e, f, prob = point.split("-", 2)
      prob = float(prob)
      if prob >= threshold:
        if inv:
          e, f = f, e
        if hard:
          print "%s-%s" % (e, f),
        else:
          print "%s-%s-%.3lf" % (e, f, prob),
      
    print
