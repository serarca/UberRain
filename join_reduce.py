#!/usr/bin/env python3

import sys
import csv

def merge_data(var_name,out_dict,in_dict):
    out_dict[var_name] = in_dict[var_name]
    return

#Input from stdin
in_file = csv.reader(sys.stdin,delimiter='\t')
input_header = ['join_key','medallion','hack_license','pickup_datetime','dropoff_datetime','passenger_count','trip_time_in_secs','trip_distance','fare_amount','total_fare','dataset']
output_header = ['join_key','medallion','hack_license','pickup_datetime','dropoff_datetime','passenger_count','trip_time_in_secs','trip_distance','fare_amount','total_fare']

output = {}
last_join_key = ''
for line in in_file:
    dict = {input_header[i]:line[i] for i in range(0,len(line))}

    #Pull variables
    var_list = ['join_key','medallion','hack_license','pickup_datetime']
    for var in var_list:
        merge_data(var,output,dict)
    #Pull variables from dataset 1
    if int(dict['dataset'])==1:
        var_list = ['dropoff_datetime','passenger_count','trip_time_in_secs','trip_distance']
        for var in var_list:
            merge_data(var,output,dict)
    #Pull variables from dataset 2
    elif int(dict['dataset'])==2:
        var_list = ['fare_amount','total_fare']
        for var in var_list:
            merge_data(var,output,dict)
    if last_join_key == dict['join_key']:
        merged_output = []
        for x in output_header:
            merged_output.append(output[x])
        print('\t'.join(merged_output))
    last_join_key = dict['join_key']
