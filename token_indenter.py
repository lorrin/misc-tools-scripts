#!/usr/bin/env python

# Looks at token in a particular position in each line and indents the line
# differently for each unique identifier found in the file. For example, given
# a log file which contains a thread identifier, contents for each thread will
# be separated out into distinct columns.
#
# Lines not matching the pattern (e.g. stack traces) are presumed to have
# occurred at the time of and belong to the same identifier as the preceding line.
#
# Default pattern is: <date> <stamp> ignored [thread_id] <message>
# Yielding output: <stamp><tabs><message>
#
# An alternate regular expression can be supplied on the command line; it must
# include named capture groups 'stamp', 'id', and 'message'. The default regex
# is: ^\S+ (?P<stamp>\S+) \S+ \[(?P<id>[^\]]+)\] (?P<message>.*)
#
# If the input contains very long lines it can be helpful to truncate them
# beforehand by e.g. piping through awk '{print substr($0,0,400)}'

import sys,re
if len(sys.argv) > 1:
  pattern = re.compile(sys.argv[1])
else:
  pattern = re.compile('^\S+ (?P<stamp>\S+) \S+ \[(?P<id>[^\]]+)\] (?P<message>.*)')

delimiter='\t'
max_level = 1
categories = {}
legend = None
indent = ""
stamp = ""

try:
  for line in [l.strip() for l in sys.stdin]:
    m = pattern.match(line)
    if m: 
      stamp,identifier,message = [m.group(x) for x in ['stamp','id','message']]
      indent = categories.get(identifier)
      if not legend:
        legend = " " * len(stamp)
      if not indent:
        indent = delimiter * max_level 
        categories[identifier] = indent
        max_level += 1
        legend += delimiter + identifier
      print stamp + indent + message
    else:
      # carry over stamp and indent from previous line
      print stamp + indent + line

  print legend
except IOError:
  pass
