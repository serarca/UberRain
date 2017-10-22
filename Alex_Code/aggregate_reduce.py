import sys
import csv

in_file = csv.reader(sys.stdin, delimiter=',')

in_header = ['key', 'date', 'hour', 'hack', 't_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings']
out_header = ['date', 'hour', 'drivers_onduty' 't_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings'] 

# initialize variables
last_key = None
master_array = []	
key = ""
counter = 1
# formates array
def format_line(line):
	formatted = []
	for i in range(len(in_header)):
		if (i >= 3):
			try: 
				value = int(line.pop(0))
			except ValueError:
				pass
				
		else:
			value = line.pop(0)
		formatted.append(value)
	return formatted

# Aggregates line 
#def process(master_array, array):
#	global master_array
#	if (len(master_array) == 0):
#		master_array = array
#	else:
#		for i in range(3, len(in_header)):
#			master_array[i] += array[i]		 
#	return array

# streaming file line by line	
for line in in_file:
#	global master_array
	key = line[0]
	# formats line
	line = format_line(line)
	
	# if first entry
	if not last_key:
		last_key = key
		master_array = line

	if (key == last_key):
		for i in range(3, len(in_header)):
			master_array[i] += line[i]
#		master_array = process(master_array, line)
		print("TINDER MATCH")	
		print(master_array)

	else:
		print("FINAL GROUP")
		print(master_array)
		master_array = line	
		last_key = key
