PATH = "YOUR_PATH/files/events.json"

"""
Merutochan
http://merutochan.it
any reference to Death Note is purely coincidental

"""

# LIBRARIES
import json
import sys
import re
import collections
import colored
import time
import os

# Create a named tuple for the "events"
definedEvent = collections.namedtuple('Event', ['name', 'desc', 'date', 'time',
                                          'place'])
# Colored
COLOR = colored.fg(226)
COLOR2 = colored.fg(6)
COLOR3 = colored.fg(4)
COLOR4 = colored.fg(82)
RESET = colored.attr('reset')

# FUNCTIONS

def shellInterface():
    inp = input("defnotes >> ")
    
    # I split "" so I can treat parameters
    inpS = re.split("\" | '", inp)
    # I split inpS[0] again, which should give the actual input I need
    inpSS = inpS[0].split()
 
    # Execute input
    if (not inp):
        pass
    elif (inpSS[0] == "exit" or inpSS[0] == "quit"):
        quit()
    
    elif (inpSS[0] == "help"):
        print(COLOR+"Notes and Events Scheduler Script - Merutochan"+RESET)
        print(COLOR3+"(http://merutochan.it)"+RESET)
        print("\n\n")
        print(COLOR2+"'add'"+RESET+" : add an event to the list.")
        print(COLOR2+"\tadd 'name' 'description' date time 'place'")
        print(COLOR2+"'remove'"+RESET+" : remove an event from the list.")
        print(COLOR2+"\t-d"+RESET+" : remove all events in a certain date.")
        print(COLOR2+"\t-t"+RESET+" : remove all events at a certain time.")
        print(COLOR2+"'ls'"+RESET+" : lists all the events from the list.")
        print(COLOR2+"'clear'"+RESET+" : removes all the events from the list.")
        print(COLOR2+"'help' :"+RESET+" shows this. ;)")
        print(COLOR2+"'exit' / 'quit' :"+RESET+" quit this program.")
        print(RESET)
    
    elif (inpSS[0] == "add"):
        if (len(inpSS)==1):
            newEvent()
        else:
            print("Wrong number of arguments! Use only '"+inpSS[0]+"'.")
    # REMOVE
    elif (inpSS[0] == "rm"):
        removeEvent(inp)
    # LS
    elif (inpSS[0] == "ls"):
        listAllEvents()
    # CLEAR
    elif (inpSS[0] == "clear"):
        clear()
    else:
        print("Invalid input! Use 'help' to get help.")
    shellInterface()
    return

# ADD EVENT
def newEvent():
	try:
		with open(PATH, 'r') as j_data:
			d = json.load(j_data)
	except IOError:
		print("Could not open the file " + PATH + " (READ)")
		
	print(d)
	
	# User input
	eventName = input("Insert the name of the event: ")
	if ((not eventName)):
		print("Error! Content was blank!")
		shellInterface()
	eventDesc = input("Insert the description of the event: ")
	eventDate = input("Insert the date of the event (dd/mm/yyyy): ")
	eventTime = input("Insert the time of the event: ")
	eventPlace = input("Insert the place of the event: ")
	
	x = {"Name":eventName,"Desc":eventDesc,"Date":eventDate,"Time":eventTime,"Place":eventPlace}
	
	# Put element in order
	position = 0
	for e in d['events']:
		if (not eventDate):
			break
		elif (not e['Date']):
			position+=1
			continue
		# CHECK YEAR, MONTH, DAY, HOUR, MINUTE
		elif(int(eventDate.split("/")[2]) >
		int(e['Date'].split("/")[2])):
			position+=1
			continue
		elif(int(eventDate.split("/")[1]) >
		int(e['Date'].split("/")[1])):
			position+=1
			continue
		elif(int(eventDate.split("/")[0]) >
		int(e['Date'].split("/")[0])):
			position+=1
			continue
		elif(int(eventTime.split(":")[0]) >
		int(e['Time'].split(":")[0])):
			position+=1
			continue
		elif(int(eventTime.split(":")[1]) >
		int(e['Time'].split(":")[1])):
			position+=1
			continue
		else:
			break
	
	d['events'].insert(position, x)
	
	print(d)
	
	try:
		with open(PATH, "w") as j_data:
			json.dump(d, j_data, indent=4, sort_keys=True)
	except IOError:
		print("Could not open the file " + PATH + " (WRITE)")

	return
	

# SHOW ALL EVENTS
def listAllEvents():
	shown = 0
	# Read file
	try:
		with open(PATH, "r") as j_data:
			d = json.load(j_data)
	except IOError:
		print("Could not open the file " + PATH + " (READ)")
	
	# LIST
	for e in d['events']:
		if(not e['Date']):
			print(colored.fg(5) + e['Name'] + RESET)
			print(e['Desc'])
			shown+=1
		else:
			print(COLOR +"[" + e['Date'] + "] " + RESET + COLOR2 + "(" + e['Time'] +
			") " + RESET + COLOR3 + e['Name'] + RESET + COLOR4 + " @ ["+e['Place']+"]" + RESET)
			print(e['Desc'])
			shown+=1
	if (shown == 0):
		print("There are no events to show.")
	return

# CLEAR ALL EVENTS
def clear():
	# Read file
	try:
		with open(PATH, "w") as j_data:
			d = { "events" :  [] }
			json.dump(d, j_data)
			print("Cleared all event(s).")
	except IOError:
		print("Could not open the file " + PATH + " (WRITE)")
	return


# REMOVE EVENT
def removeEvent(mode):
	# Read file
	try:
		with open(PATH, "r") as j_data:
			d = json.load(j_data)
	except IOError:
		print("Could not open the file " + PATH + " (READ)")

	modeSplit = mode.split()
	# SINGLE MODE (REMOVE BY NAME)
	if (len(modeSplit)==1):
		toBeRemoved = input("Insert the name of the event to be removed: ")
		for e in d['events']:
			if (e["Name"] == toBeRemoved):
				d['events'].remove(e)
				# Rewrite file
				try:
					with open(PATH, "w") as j_data:
						json.dump(d, j_data)
						print("Event removed.")
						break
				except IOError:
					print("Could not open the file " + PATH + " (WRITE)")
				return
		print("No matching event was found.")
		

    # DATE MODE
	elif (modeSplit[1]=="-d" and len(modeSplit)==3):
		for e in d['events']:
			if (e['Date'] == modeSplit[2]):
				d['events'].remove(e)
				# Rewrite file
				try:
					with open(PATH, "w") as j_data:
						json.dump(d, j_data)
						print("Event removed.")
				except IOError:
					print("Could not open the file " + PATH + " (WRITE)")
		print("No matching event was found.")
                

    # TIME MODE
	elif (modeSplit[1]=="-t" and len(modeSplit)==3):
		for e in d['events']:
			if (e['Time'] == modeSplit[2]):
				d['events'].remove(e)
				# Rewrite file
				try:
					with open(PATH, "w") as j_data:
						json.dump(d, j_data)
						print("Event removed.")
				except IOError:
					print("Could not open the file " + PATH + " (WRITE)")
		print("No matching event was found.")
    # ERROR
	else:
		print("Wrong use of parameters/arguments! Use 'help' to have more info"+
		" about the use of the 'remove' function.")
	return


# CHECK FOR THE PASSED EVENTS, REMOVE THEM
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
if (len(sys.argv)==1):
    checkExpired()
    shellInterface()
else:
    print("Error.")
    print("Wrong number of arguments! Use only defschedule.")
