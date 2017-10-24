#!/usr/bin/env python3

import sys

# headers
in_header = ['key', 'date', 'hour', 'hack', 't_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings']
out_header = ['date', 'hour', 'drivers_onduty' 't_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings'] 

# initialize variables
last_key = None
master_array = []	
key = ""
driver_count = 1

# formates array, converts values from str to floats for indices 4:10
def format_line(line):
    line = line.rstrip().split("\t")
    formatted = []
    for i in range(len(in_header)):
        if(i >= 4):
            value = float(line.pop(0))
        else:
            value = line.pop(0)
        formatted.append(value)
    return formatted

# streaming
for line in sys.stdin:
    # formats line
    line = format_line(line)

    key = line[0]
	
    # if first entry
    if last_key == None:
        last_key = key
        master_array = line
	
    # if key match
    elif (key == last_key):
        driver_count += 1

        # aggregate all statistics
        for i in range(4 , len(in_header)):
            master_array[i] += line[i]
 
   # if new group (hour), print results of previous group 
    else:
        # string values
        line1 = ('{0}\t{1}\t{2}'.format(master_array[1], master_array[2], str(driver_count)))
        # float values
        line2 =	('\t'.join(str(master_array[i]) for i in range(4, len(master_array))))
        print(line1 + "\t" + line2)
        # Reset for next group
        master_array = line	
        last_key = key
        driver_count = 1

# print results for final group
line1 = ('{0}\t{1}\t{2}'.format(master_array[1], master_array[2], str(driver_count)))
line2 = ('\t'.join(str(master_array[i]) for i in range(4, len(master_array))))
print(line1 + "\t" + line2)
