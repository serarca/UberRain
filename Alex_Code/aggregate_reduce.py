import sys
import csv

in_file = csv.reader(sys.stdin, delimiter=',')

in_header = ['key', 'date', 'hour', 'hack', 't_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings']
out_header = ['date', 'hour', 'drivers_onduty' 't_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings'] 

# initialize variables
last_key = None
master_array = []	
key = ""
driver_count = 1
# formates array

def format_line(line):
	formatted = []
	for i in range(len(in_header)):
		if (i >= 4):
			try: 
				value = int(line.pop(0))
			except ValueError:
				pass
		else:
			value = line.pop(0)
		formatted.append(value)
	return formatted


# streaming
for line in in_file:
	key = line[0]

	# formats line
	line = format_line(line)
	
	# if first entry
	if not last_key:
		last_key = key
		master_array = line
	
	# if key match
	if (key == last_key):
		driver_count += 1

		# aggregate
		for i in range(3, len(in_header)):
			master_array[i] += line[i]
	else:
		line1 = ('{0},{1},{2}'.format(master_array[1], master_array[2], str(driver_count)))
		line2 =	(','.join(str(master_array[i]) for i in range(4, len(master_array))))
		print(line1 + "," + line2)
		master_array = line	
		last_key = key
		driver_count = 1
# output header
print(','.join(out_header[i] for i in range(len(out_header))))
