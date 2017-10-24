#!/usr/bin/python

import sys
import csv

in_file = csv.reader(sys.stdin, delimiter='\t')

header = ['date', 'hour', 'hack', 't_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings']

for line in in_file:
    dict = {header[i]:line[i] for i in range(len(line))}
    key = dict['date'] + ' ' +  dict['hour']
    print (key + '\t' + '\t'.join(line))
