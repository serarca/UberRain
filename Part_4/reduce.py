import sys
from datetime import datetime, timedelta
from dateutil import parser

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

    sorted_array = sorted(driver_array, key = lambda line:parser.parse(
        line["pickup_datetime"]).strftime("%Y-%m-%d %H"))

    # Correct errors
    for i in range(0, len(sorted_array)):
        pickup_time = parser.parse(sorted_array[i]['pickup_datetime'])
        dropoff_time = parser.parse(sorted_array[i]['dropoff_datetime'])

        if (dropoff_time<pickup_time):
            sorted_array[i]['dropoff_datetime'] = pickup_time.strftime("%Y-%m-%d %H:%M:%S")
        if (i<len(sorted_array)-1):
            next_pickup_time = parser.parse(sorted_array[i + 1]['pickup_datetime'])
            if (dropoff_time > next_pickup_time):
                sorted_array[i + 1]['pickup_datetime'] = dropoff_time.strftime("%Y-%m-%d %H:%M:%S")

    # Construct result dictionary
    first_hour = parser.parse(sorted_array[0]['pickup_datetime']).strftime("%Y-%m-%d %H")
    final_hour = parser.parse(sorted_array[len(sorted_array)-1]['dropoff_datetime']).strftime("%Y-%m-%d %H")
    results = {}
    while first_hour <= final_hour:
        results[first_hour] = {'not_on_duty':0.0, "time_with_passengers":0.0,
                                "passengers_picked_up":0.0, "trips_started": 0.0,
                                "miles":0.0, "earnings":0.0}
        first_hour = (parser.parse(first_hour) + timedelta(hours = 1)).strftime("%Y-%m-%d %H")

    # Fill results
    last_dropoff = parser.parse(sorted_array[0]['pickup_datetime'])
    for i in range(0, len(sorted_array)):
        # Extract details
        pickup_time = parser.parse(sorted_array[i]['pickup_datetime'])
        dropoff_time = parser.parse(sorted_array[i]['dropoff_datetime'])
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
                results[begin_rest]['not_on_duty'] += intersection(
                parser.parse(begin_rest), last_dropoff, pickup_time)
                begin_rest = (parser.parse(begin_rest)
                            + timedelta(hours = 1)).strftime("%Y-%m-%d %H")

        # Check how much time with passengers, how much money and how many miles
        begin_ride = pickup_time.strftime("%Y-%m-%d %H")
        end_ride = dropoff_time.strftime("%Y-%m-%d %H")
        while (begin_ride <= end_ride):
            time_with_passengers = intersection(
                parser.parse(begin_ride), pickup_time, dropoff_time)
            results[begin_ride]["time_with_passengers"] += time_with_passengers
            results[begin_ride]["miles"] += ((timedelta(hours = time_with_passengers).total_seconds()/total_time.total_seconds()) *
                float(sorted_array[i]['trip_distance']))
            results[begin_ride]["earnings"] += ((timedelta(hours = time_with_passengers).total_seconds()/total_time.total_seconds()) *
                    float(sorted_array[i]['total_fare']))

            begin_ride = (parser.parse(begin_ride)
                        + timedelta(hours = 1)).strftime("%Y-%m-%d %H")

        # How many passengers picked up and trips started
        begin_ride = pickup_time.strftime("%Y-%m-%d %H")
        results[begin_ride]["passengers_picked_up"] += int(sorted_array[i]['passenger_count'])
        results[begin_ride]["trips_started"] += 1
        #pdb.set_trace()
        last_dropoff = dropoff_time

    for k in results.keys():
        print ('\t'.join([k,sorted_array[0]['key']]+[str(results[k][x]) for x in keys_result]))





header = ['key','medallion_hack_license_pickup_datetime', 'medallion',
    'hack_license', 'pickup_datetime', 'dropoff_datetime', 'passenger_count',
    'trip_time_in_secs', 'trip_distance', 'fare_amount', 'total_fare']
key = ""
driver_array = []

keys_result = ['trips_started', 'earnings', 'miles', 'passengers_picked_up', 'not_on_duty', 'time_with_passengers']

print ("\t".join(['hour','key','trips_started', 'earnings', 'miles', 'passengers_picked_up', 'not_on_duty', 'time_with_passengers']))
with open("mapped_ordered.csv", "r") as ins:
    for line in ins:
#for line in sys.stdin:
        formatted = line.rstrip().split("\t")
        formatted_dict = {header[i]:formatted[i] for i in range(0, len(header))}
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
