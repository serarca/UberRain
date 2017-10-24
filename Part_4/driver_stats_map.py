#!/usr/bin/python

import sys

header = ['join_key','medallion','hack_license','pickup_datetime','dropoff_datetime','passenger_count','trip_time_in_secs','trip_distance','fare_amount','total_fare']

for line in sys.stdin:
    line = line.rstrip().split("\t")
    dict = {header[i]:line[i] for i in range(0, len(header))}
    #Use hack license as key
    line[0] = dict['hack_license']
    print ('\t'.join(line))
