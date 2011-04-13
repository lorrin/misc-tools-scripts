#!/usr/bin/env python

# Selects time range from a log file. Lines with no time (e.g. stack traces)
# are presumed to have occurred at the time of the preceding line.
# 
# Assumes first time-like phrase on a line is the timestamp for that line.
#
# Assumes time format is pairs of digits separated by colons with optional , or
# . initiated suffix. E.g. HH:mm:ss,SSS, HH:mm, etc.
#
# Does not strip blank lines; just use awk 'NF>0' for that.

import sys,re
time_pattern = re.compile("(?:^|.*?\D)(\d{1,2}(?::\d{2})+(?:[,.]\d+)?)")
fields_pattern = re.compile("[:,.]")

if len(sys.argv) < 3:
  print >> sys.stderr, "Please specify start and end times (e.g. %s 13:50 14:10:01,101)." % sys.argv[0]
  exit(1)

for item,index in [["start time",1],["end time",2]]:
  if not time_pattern.match(sys.argv[index]):
    raise ValueError("Cannot parse %s: %s" % (item, sys.argv[index]))

start,end = [[int(x) for x in re.split(fields_pattern, s)] for s in sys.argv[1:3]]
too_soon = True

try:
  for line in sys.stdin:
    line = line.strip()
    m = time_pattern.match(line)
    if m:
      t = [int(x) for x in re.split(fields_pattern,m.group(1))]
      if t >= end:
        break
      elif too_soon and t >= start:
        too_soon = False

    if not too_soon:
      print line
except IOError:
  pass
