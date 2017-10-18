import sys
from datetime import datetime, timedelta
from dateutil import parser



header = sys.stdin.readline().rstrip().split(",")
print(header)

for line in sys.stdin:
    formatted = line.rstrip().split(",")
    formatted_dict = {header[i]:formatted[i] for i in range(0, len(header))}
    #dropoff = parser.parse(formatted_dict['dropoff_datetime'])
    #pickup = parser.parse(formatted_dict['pickup_datetime'])

    #dropoff_hour = parser.parse(dropoff.strftime("%Y-%m-%d %H"))
    #pickup_hour = parser.parse(pickup.strftime("%Y-%m-%d %H"))



    #while (dropoff_hour>=pickup_hour):
    #    print ('\t'.join([formatted_dict['hack_license'] + " " + pickup_hour.strftime("%Y-%m-%d %H")] + formatted))
    #    pickup_hour = pickup_hour + timedelta(hours = 1)

    print ('\t'.join([formatted_dict['hack_license']] + formatted))
