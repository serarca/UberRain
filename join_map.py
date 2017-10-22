#!/usr/bin/python

import sys
import csv

#Input from stdin
in_file = csv.reader(sys.stdin,delimiter='\t')

output_header = ['join_key','medallion','hack_license','pickup_datetime','dropoff_datetime','passenger_count','trip_time_in_secs','trip_distance','fare_amount','total_fare','dataset']

for line in in_file:
	dict = {}
        #Determine file by length (fare table has 12 columns)
	if len(line) <= 11:
	    header = ['medallion','hack_license','vendor_id','pickup_datetime','payment_type','fare_amount','surcharge','mta_tax','tip_amount','tolls_amount','total_amount']
	    dict = {header[i]:line[i] for i in range(0,len(line))}
	    dict['dataset']=2
	    try:
	        dict['total_fare'] =float(dict['fare_amount']) + float(dict['tip_amount'])
	    except ValueError:
	        continue
	#Trip data table
	else:
	    header = ['medallion','hack_license','vendor_id','rate_code','store_and_fwd_flag','pickup_datetime','dropoff_datetime','passenger_count','trip_time_in_secs','trip_distance','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude']
	    dict = {header[i]:line[i] for i in range(0,len(line))}
	    dict['dataset']=1

	#Join key
	dict['join_key'] = dict['medallion'] + '_' + dict['hack_license'] + '_' + dict['pickup_datetime']

	# write the results to STDOUT (standard output);
	output = []
	for x in output_header:
	    try:
    	        output.append(str(dict[x]))
	    except KeyError:
	        output.append('-')
	print('\t'.join(output))
