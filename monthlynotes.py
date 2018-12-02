#!/usr/bin/python3
PATH = "YOUR_PATH/events.json"
"""
Merutochan
http://merutochan.it

"""
# LIBRARIES
import json
import colored
import time

try:
	with open(PATH, 'r') as j_data:
		d = json.load(j_data)
except IOError:
	print("Could not open the file " + PATH + " (READ)")
	quit()
		
# COLORS
color = colored.fg(226)
color2 = colored.fg(120)
color3 = colored.fg(87)
color4 = colored.fg(82)
color5 = colored.fg(5)
r = colored.attr('reset')

# CHECK EXPIRED EVENTS
def checkExpired():
	# Read file
	try:
		with open(PATH, "r") as j_data:
			d = json.load(j_data)
	except IOError:
		print("Could not open the file " + PATH + " (READ)")

	erased = 0
	for e in d['events']:
		if (not e['Date']):
			continue
		year = int(e['Date'].split("/")[2])
		month = int(e['Date'].split("/")[1])
		day = int(e['Date'].split("/")[0])
		hour = int(e['Time'].split(":")[0])
		minu = int(e['Time'].split(":")[1])
        # Check on year
		if (year<int(time.strftime("%Y"))):
			d['events'].remove(e)
			erased+=1
		elif (year==int(time.strftime("%Y"))):
			# Check on month
			if (month<int(time.strftime("%m"))):
				d['events'].remove(e)
				erased+=1
			elif (month==int(time.strftime("%m"))):
				# Check on day
				if (day<int(time.strftime("%d"))):
					d['events'].remove(e)
					erased+=1            
				elif (day==int(time.strftime("%d"))):
					# Check on hour
					if (hour<int(time.strftime("%H"))):
						d['events'].remove(e)
						erased+=1
					elif (hour==int(time.strftime("%H"))):
						# Check on minute
						if (minu<int(time.strftime("%M"))):
							d['events'].remove(e)
							erased+=1
		else:
			continue
	if (erased > 0):
		# Rewrite file
		try:
			with open(PATH, "w") as j_data:
				json.dump(d, j_data)
		except IOError:
			print("Could not open the file " + PATH + " (WRITE)")
		print("Removed " + str(erased) + " past events.")
	return

# EXECUTION CODE

checkExpired()
# Re-read
try:
	with open(PATH, 'r') as j_data:
		d = json.load(j_data)
except IOError:
	print("Could not open the file " + PATH + " (READ)")
	quit()

for e in d['events']:
    # SHOW THE EVENTS OF THE SAME MONTH
    if(not e['Date']):
        print(color5+e['Name']+r)
        print(color3+e['Desc']+r)
        print()
    elif(e['Date'].split("/")[1] == time.strftime("%m")):
        print(color5+e['Name']+r)
        print(color+"["+e['Date']+"] "+r+color2+"("+e['Time']+") "+r+
        color3+e['Desc']+r+color4+" @ ["+e['Place']+"]"+r)
        print()
