#!/usr/bin/python

import sys

header = ['date', 'hour', 'hack', 't_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings']

for line in sys.stdin:
    line = line.rstrip().split("\t")
    dict = {header[i]:line[i] for i in range(len(line))}
    key = dict['date'] + ' ' +  dict['hour']
    print (key + '\t' + '\t'.join(line))
