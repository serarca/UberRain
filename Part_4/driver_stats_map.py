#!/usr/bin/python

import sys
import csv

header = ['join_key','medallion','hack_license','pickup_datetime','dropoff_datetime','passenger_count','trip_time_in_secs','trip_distance','fare_amount','total_fare']
in_file = csv.reader(sys.stdin,delimiter='\t')

for line in in_file:
    dict = {header[i]:line[i] for i in range(0, len(header))}
    line[0] = dict['hack_license']
    print ('\t'.join(line))
