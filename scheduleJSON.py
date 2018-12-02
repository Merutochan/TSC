PATH = 'YOUR_PATH/fles/scheduling.json'

"""
Merutochan
http://merutochan.it

"""
# LIBRARIES
import time
import json
import colored

# COLORS
color = colored.fg(226)
color2 = colored.fg(120)
color3 = colored.fg(87)
color4 = colored.fg(82)
reset = colored.attr('reset')
	
# FUNCTIONS
# Parse day events
def dayschedule(n):
	for day in d['events']['week']:
		# Check if week day matches
		if (day['n'] == n):
			# If it is a work day
			print(color + day['Name'] + time.strftime(", %d %b %Y - ") + time.strftime("%H:%M") + reset+"\n")
			if (day['Work']):
				for e in day['Schedule']:
					print('[' + color2 + e['start'] + reset+ '~' + color2 + e['end'] + reset + ']')
					print(color3 + e['what'] + reset + ' - ' + color4 + e['where'] + reset)
			else:
				print(color3 + "Today is a free day." + reset)
				print(color2 + "Enjoy it while it lasts." + reset)

# Parse birthdays
def birthdays(date):
	counter=0
	for b in d['events']['year']['birthdays']:
		if (b['Date'] == date):
			print("Today,", date, ", is",
				b['Name']+ "'s birthday, who is now",
				int(time.strftime("%Y")) - int(b['Year']),
				"years old!")
			counter+=1
	return counter
	
# Parse holidays
def holidays(date):
	counter = 0
	for h in d['events']['year']['holidays']:
		if (h['Date'] == date):
			print("Today,", date, ", is", h['Name']+
				".", h['Message'])
			counter +=1
	return counter
	
# MAIN
				
with open(PATH) as j_data:
	d = json.load(j_data)
	dayschedule(time.strftime("%w"))
	if (birthdays(time.strftime("%d/%m"))):
		print()
	if (holidays(time.strftime("%d/%m"))):
		print()
	
