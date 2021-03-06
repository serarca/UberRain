#!/usr/bin/python

import sys
from datetime import datetime, timedelta

# This function calculates the intersection between an hour and an interval
def intersection(hour, beg_interval, end_interval):
    end_hour = hour + timedelta(hours = 1)
    if (beg_interval >= end_hour or end_interval <= hour):
        return 0.0
    elif (beg_interval <= hour and end_interval >= end_hour):
        return 1.0
    elif (beg_interval >= hour and end_interval >= end_hour):
        return (end_hour - beg_interval).total_seconds()/timedelta(hours = 1).total_seconds()
    elif (beg_interval <= hour and end_interval <= end_hour):
        return (end_interval - hour).total_seconds()/timedelta(hours = 1).total_seconds()
    elif (beg_interval >= hour and end_interval <= end_hour):
        return (end_interval - beg_interval).total_seconds()/timedelta(hours = 1).total_seconds()
    else:
        return -1


def process_array(driver_array):

    sorted_array = sorted(driver_array, key=lambda line:datetime.strptime(
        line["pickup_datetime"],'%Y-%m-%d %H:%M:%S'))

    # Correct errors - account for overlapping trips (data entry errors)
    for i in range(0, len(sorted_array)):
        pickup_time = datetime.strptime(sorted_array[i]['pickup_datetime'],'%Y-%m-%d %H:%M:%S')
        dropoff_time = datetime.strptime(sorted_array[i]['dropoff_datetime'],'%Y-%m-%d %H:%M:%S')
        if (dropoff_time<pickup_time):
            sorted_array[i]['dropoff_datetime'] = pickup_time.strftime("%Y-%m-%d %H:%M:%S")
        if (i<len(sorted_array)-1):
            next_pickup_time = datetime.strptime(sorted_array[i + 1]['pickup_datetime'],'%Y-%m-%d %H:%M:%S')
            if (dropoff_time > next_pickup_time):
                sorted_array[i]['dropoff_datetime'] = pickup_time.strftime("%Y-%m-%d %H:%M:%S")

        # Check for impossible speeds
        # (Greater than speed limit of 65mph, and correct miles traveled to upper limit)
        travel_time = dropoff_time - pickup_time
        trip_distance = float(sorted_array[i]['trip_distance'])
        if(travel_time.total_seconds() > 0):
            if (trip_distance / (travel_time.total_seconds()/3600) > 65):
                sorted_array[i]['trip_distance'] = str(65 * travel_time.total_seconds()/3600)

    # Construct result dictionary (one entry for each hour)
    first_hour = datetime.strptime(sorted_array[0]['pickup_datetime'],'%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H")
    final_hour = datetime.strptime(sorted_array[len(sorted_array)-1]['dropoff_datetime'],'%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H")
    results = {}
    while first_hour <= final_hour:
        results[first_hour] = {"not_on_duty":0.0, "t_occupied":0.0,
                                "n_pass":0.0, "n_trip": 0.0,
                                "n_mile":0.0, "earnings":0.0}
        first_hour = (datetime.strptime(first_hour,'%Y-%m-%d %H') + timedelta(hours = 1)).strftime("%Y-%m-%d %H")

    # Fill results
    last_dropoff = datetime.strptime(sorted_array[0]['pickup_datetime'],'%Y-%m-%d %H:%M:%S')

    # Loop through rides
    for i in range(0, len(sorted_array)):
        # Extract details
        pickup_time = datetime.strptime(sorted_array[i]['pickup_datetime'],'%Y-%m-%d %H:%M:%S')
        dropoff_time = datetime.strptime(sorted_array[i]['dropoff_datetime'],'%Y-%m-%d %H:%M:%S')
        total_time = dropoff_time - pickup_time
        if (total_time.total_seconds()==0):
            last_dropoff = dropoff_time
            continue

        # Check if driver is on duty and add it to results
        on_duty = (pickup_time - last_dropoff < timedelta(minutes = 30))
        if (not on_duty):
            begin_rest = last_dropoff.strftime("%Y-%m-%d %H")
            end_rest = pickup_time.strftime("%Y-%m-%d %H")
            while (begin_rest <= end_rest):
                results[begin_rest]['not_on_duty'] += intersection(datetime.strptime(begin_rest,'%Y-%m-%d %H'), last_dropoff, pickup_time)
                begin_rest = (datetime.strptime(begin_rest,'%Y-%m-%d %H') + timedelta(hours = 1)).strftime("%Y-%m-%d %H")
        last_dropoff = dropoff_time

        # Check how much time with passengers, how much money and how many miles
        begin_ride = pickup_time.strftime("%Y-%m-%d %H")
        end_ride = dropoff_time.strftime("%Y-%m-%d %H")
        while (begin_ride <= end_ride):
            t_occupied = intersection(
                datetime.strptime(begin_ride,'%Y-%m-%d %H'), pickup_time, dropoff_time)
            results[begin_ride]["t_occupied"] += t_occupied
            results[begin_ride]["n_mile"] += ((timedelta(hours = t_occupied).total_seconds()/total_time.total_seconds()) *
                float(sorted_array[i]['trip_distance']))
            results[begin_ride]["earnings"] += ((timedelta(hours = t_occupied).total_seconds()/total_time.total_seconds()) *
                float(sorted_array[i]['total_fare']))
            begin_ride = (datetime.strptime(begin_ride,'%Y-%m-%d %H') + timedelta(hours = 1)).strftime("%Y-%m-%d %H")

        # How many passengers picked up and trips started
        begin_ride = pickup_time.strftime("%Y-%m-%d %H")
        results[begin_ride]["n_pass"] += int(sorted_array[i]['passenger_count'])
        results[begin_ride]["n_trip"] += 1

    for k in results.keys():
        results[k]['date'] = k[0:10]
        results[k]['hour'] = k[11:13]
        results[k]['hack'] = sorted_array[0]['hack_license']
        results[k]['t_onduty'] = 1 - results[k]['not_on_duty']
        #Print results if time on duty is greater than zero
        if(results[k]['t_onduty'] > 0):
            print ('\t'.join([str(results[k][x]) for x in keys_result]))



header = ['key', 'medallion',
    'hack_license', 'pickup_datetime', 'dropoff_datetime', 'passenger_count',
    'trip_time_in_secs', 'trip_distance', 'fare_amount', 'total_fare']
key = ""
driver_array = []

keys_result = ['date','hour','hack','t_onduty','t_occupied','n_pass','n_trip','n_mile','earnings']

for line in sys.stdin:
    formatted = line.rstrip().split("\t")
    formatted_dict = {header[i]:formatted[i] for i in range(0, len(header))}

    # Check formats of data fields used in calculations. If error, skip observation.
    try:
        pickup_datetime = datetime.strptime(formatted_dict['pickup_datetime'],'%Y-%m-%d %H:%M:%S')
        dropoff_datetime = datetime.strptime(formatted_dict['dropoff_datetime'],'%Y-%m-%d %H:%M:%S')
        passenger_count = float(formatted_dict['passenger_count'])
        trip_distance = float(formatted_dict['trip_distance'])
        total_fare = float(formatted_dict['total_fare'])
    except ValueError:
        continue

    # Check the key
    new_key = formatted_dict['key']
    if new_key!=key:
        # Process previous array
        if(len(driver_array)!=0):
            process_array(driver_array)
        # Empty array
        driver_array = [formatted_dict]
        # Set up new key
        key = new_key
    else:
        # Add line to array
        driver_array += [formatted_dict]

# Process the last driver
process_array(driver_array)
