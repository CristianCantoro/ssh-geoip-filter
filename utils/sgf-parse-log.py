#!/usr/bin/env python3
"""Parse timestamps from log file to convert it to ISO.

Usage:
  sgf-parse-log.py [--tz TIMEZONE] [--time-format=TIME_FORMAT]...
                   [<logfile>]...
  sgf-parse-log.py (-h | --help)
  sgf-parse-log.py --version

Argiments:
  <logfile>       Log file to read [default: stdin].

Options:
  --tz TIMEZONE               Timezone of the timestamps in the log file.
  --time-format=TIME_FORMAT   Time format of the timestamps in the log file.
                              It can be specified multiple times.
  -h --help                   Show this screen.
  --version                   Show version.
"""
import sys
import arrow
import dateutil
from docopt import docopt


def read_input(logfile):
    if not logfile:
        lines = sys.stdin.readlines()
        for line in lines:
          yield(line)
    else:
      for infile in arguments['<logfile>']:
        infp = open(infile, 'r')
        for line in infp:
          yield(line)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='sgf-stats.py 0.0.1')

    logfile = arguments['<logfile>']
    tz = arguments['--tz']
    time_formats = arguments['--time-format']

    for line in read_input(logfile):    

      line = line.split()

      year = arrow.now().year
      month = line[0]
      day = line[1]
      time = line[2]

      country = line[-1].strip('()')
      ip_address = line[-2]

      
      timestamp = arrow.get('{year} {month} {day} {time}'.format(year=year,
                                                                 month=month,
                                                                 day=day,
                                                                 time=time),
                            [tf for tf in time_formats]
                            ).replace(tzinfo=dateutil.tz.gettz(tz))

      print(timestamp, country, ip_address)
