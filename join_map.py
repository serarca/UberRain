#!/usr/bin/python

import sys
import csv

#Input from stdin
in_file = csv.reader(sys.stdin,delimiter=',')

for line in in_file:
	#Set defaults for all non-key fields
	dataset = "-"
	total_fare = "-"
	payment_type = "-"
	fare_amount = "-"
	surcharge = "-"
	mta_tax = "-"
	tip_amount = "-"
	tolls_amount = "-"
	total_amount = "-"
	rate_code = "-"
	dropoff_datetime = "-"
	passenger_count = "-"
	trip_time_in_secs = "-"
	trip_distance = "-"
	pickup_longitude = "-"
	pickup_latitude = "-"
	dropoff_longitude = "-"
	dropoff_latitude = "-"
	
	#Determine file by length (fare table has 12 columns)
	if len(line) <= 11:
		dataset="2"
		medallion = line[0]
		hack_license = line[1]
		pickup_datetime = line[3]
		payment_type = line[4]
		fare_amount = line[5]
		surcharge = line[6]
		mta_tax = line[7]
		tip_amount = line[8]
		tolls_amount = line[9]
		total_amount = line[10]
		try:
			total_fare = str(float(fare_amount) + float(tip_amount))
		except ValueError:
			continue
	#Trip data table
	else:
		dataset="1"
		medallion = line[0]
		hack_license = line[1]
		rate_code = line[4]
		pickup_datetime = line[5]
		dropoff_datetime = line[6]
		passenger_count = line[7]
		trip_time_in_secs = line[8]
		trip_distance = line[9]
		pickup_longitude = line[10]
		pickup_latitude = line[11]
		dropoff_longitude = line[12]
		dropoff_latitude = line[13]

	#Join key
	join_key = medallion + '_' + hack_license + '_' + pickup_datetime

	# write the results to STDOUT (standard output);
	output = (join_key,medallion,hack_license,pickup_datetime,dropoff_datetime,passenger_count,trip_time_in_secs,trip_distance,fare_amount,total_fare,dataset)
	print('\t'.join(output))
