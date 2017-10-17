#!/usr/bin/python

import sys
import csv

#Input from stdin
in_file = csv.reader(sys.stdin,delimiter=‘\t’)

#Set defaults
last_join_key = None
last_dropoff_datetime = "-"
last_passenger_count = "-"
last_trip_time_in_secs = "-"
last_trip_distance = "-"
last_total_fare = "-"
last_total_amount = "-"

for line in in_file:
	line = list(line)
	join_key = line[0]
	dataset = int(line[10])
	if dataset==1:
		last_dropoff_datetime = line[4]
		last_passenger_count = line[5]
		last_trip_time_in_secs = line[6]
		last_trip_distance = line[7]
	elif dataset==2:
		last_total_fare = line[8]
		last_total_amount = line[9]
	if last_join_key == join_key:
		line[4] = last_dropoff_datetime
		line[5] = last_passenger_count
		line[6] = last_trip_time_in_secs
		line[7] = last_trip_distance
		line[8] = last_total_fare
		line[9] = last_total_amount
		print('\t'.join(line))
	last_join_key = join_key
