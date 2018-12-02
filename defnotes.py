SMTP_SERVER='your_server'
LOGIN = 'your_user'
PASSWORD = 'your_password'
MAIL = 'your_mail'
PATH = "files/events.xml"
SEND_ICS = False
"""
Merutochan
http://merutochan.it
any reference to death note is purely coincidental

"""

# LIBRARIES
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import sys
import re
import collections
import colored
import time
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# VARIABLES

# Create a named tuple for the "events"
tuplaEvento = collections.namedtuple('Event', ['name', 'desc', 'date', 'time',
                                          'place'])
# Colored
COLOR = colored.fg(226)
COLOR2 = colored.fg(6)
COLOR3 = colored.fg(4)
COLOR4 = colored.fg(82)
RESET = colored.attr('reset')
TREE = ET.parse(PATH)
# Get root of XML file
ROOT = TREE.getroot()

# FUNCTIONS

def inpLine():
    inp = input("defnotes >> ")
    # I split "" so I can treat name, description and place as strings
    inpS = re.split("\" | '", inp)
    # I split inpS[0] again, which should give the actual input I need
    inpSS = inpS[0].split()
    # Execute input
    # EXIT
    if (not inp):
        pass
    elif (inpSS[0] == "exit" or inpSS[0] == "quit"):
        prettify()
        quit()
    # HELP
    elif (inpSS[0] == "help"):
        print(COLOR+"Notes and Events Scheduler Script - Merutochan"+RESET)
        print(COLOR3+"(http://merutochan.it)"+RESET)
        print()
        print()
        print(COLOR2+"'add'"+RESET+" : add an event to the list.")
        print(COLOR2+"\tadd 'name' 'description' date time 'place'")
        print(COLOR2+"'remove'"+RESET+" : remove an event from the list.")
        print(COLOR2+"\t-d"+RESET+" : remove all events in a certain date.")
        print(COLOR2+"\t-t"+RESET+" : remove all events at a certain time.")
        print(COLOR2+"'ls'"+RESET+" : lists all the events from the list.")
        print(COLOR2+"'clear'"+RESET+" : removes all the events from the list.")
        print(COLOR2+"'help' :"+RESET+" shows these helpful informations. ;)")
        print(COLOR2+"'exit' / 'quit' :"+RESET+" quit this program. :(")
        print(RESET)
    # ADD
    elif (inpSS[0] == "add"):
        # If with arguments
        if (len(inpS)>1):
            # GET THE INPUT ARGUMENTS
            inpSDT = inpS[4].split() # This will give me date and time
            addevent(tuplaEvento(inpS[1], inpS[3], inpSDT[0],
            inpSDT[1], inpS[5]))
        # If without arguments
        elif (len(inpSS)==1):
            addEvent(newEvent())
        else:
            print("Wrong number of arguments! Use only " + inpSS[0]+
            " or "+inpSS[0] + " 'description' 'date' 'time' 'place'.")
    # REMOVE
    elif (inpSS[0] == "remove"):
        removeEvent(inp)
    # LS
    elif (inpSS[0] == "ls"):
        listAllEvents()
    # CLEAR
    elif (inpSS[0] == "clear"):
        clear()
    else:
        print("Invalid input! Use 'help' to get help.")
    inpLine()
    return

# CREATE NEW EVENT
def newEvent():
    eventName = input("Insert the name of the event: ")
    eventDesc = input("Insert the description of the event: ")
    eventDate = input("Insert the date of the event (dd/mm/yyyy): ")
    eventTime = input("Insert the time of the event: ")
    eventPlace = input("Insert the place of the event: ")
    if ((not eventName)):
        print("Error! Content was blank!")
        inpLine()
    else:
        e = tuplaEvento(eventName, eventDesc, eventDate, eventTime, eventPlace)
        return e

# ADD EVENT
def addEvent(event):
    # Crea un nodo e setta gli attributi
    newEvent = ET.Element("event")
    newEvent.set("name", event.name)
    newEvent.set("desc", event.desc)
    newEvent.set("date", event.date)
    newEvent.set("time", event.time)
    newEvent.set("place", event.place)

    if ((event.date) and os.system("ping http://google.it")==0 and SEND_ICS):
        makeICS(event)

    # Parse the XML with a linear search in order to place the event in
    # chronological order
    parsed = 0
    for e in ROOT.findall("event"):
        if (not newEvent.get("date")):
            break
        elif (not e.get("date")):
            parsed+=1
            continue
        # CHECK YEAR, MONTH, DAY, HOUR, MINUTE
        elif(int(newEvent.get("date").split("/")[2]) >
        int(e.get("date").split("/")[2])):
            parsed+=1
            continue
        elif(int(newEvent.get("date").split("/")[1]) >
        int(e.get("date").split("/")[1])):
            parsed+=1
            continue
        elif(int(newEvent.get("date").split("/")[0]) >
        int(e.get("date").split("/")[0])):
            parsed+=1
            continue
        elif(int(newEvent.get("time").split(":")[0]) >
        int(e.get("time").split(":")[0])):
            parsed+=1
            continue
        elif(int(newEvent.get("time").split(":")[1]) >
        int(e.get("time").split(":")[1])):
            parsed+=1
            continue
        else:
            break
    # Add the node to the structure
    ROOT.insert(parsed, newEvent)
    # Overwrite XML
    TREE.write(PATH)
    print("Event saved.")
    return

# SHOW ALL EVENTS
def listAllEvents():
    shown = 0
    for e in ROOT.findall("event"):
        if(not e.get("date")):
            print(colored.fg(5)+e.get("name")+RESET)
            print(e.get("desc"))
            shown+=1
        else:
            print(COLOR+"["+e.get("date")+"] "+RESET+COLOR2+"("+e.get("time")+
            ") "+RESET+COLOR3+e.get("name")+RESET+COLOR4+
            " @ ["+e.get("place")+"]"+RESET)
            print(e.get("desc"))
            shown+=1
    if (shown == 0):
        print("There are no events to show.")
    return

# CLEAR ALL EVEBTS
def clear():
    counter = 0
    for e in ROOT.findall("event"):
        ROOT.remove(e)
        TREE.write(PATH)
        counter+=1
    print(str(counter) +" event(s) removed.")
    return

# REMOVE EVENT
def removeEvent(mode):
    # SINGLE MODE, BY NAME
    modeSplit = mode.split()
    if (len(modeSplit)==1):
        toBeRemoved = input("Insert the name of the event to be removed: ")
        for e in ROOT.findall("event"):
            if (e.get("name") == toBeRemoved):
                ROOT.remove(e)
                TREE.write(PATH)
                print("Event removed.")
                return
        print("No matching event was found.")
        
    # DATE MODE
    elif (modeSplit[1]=="-d"):
        for e in ROOT.findall("event"):
            if (e.get("date") == modeSplit[2]):
                ROOT.remove(e)
                TREE.write(PATH)
                print("Event removed.")
        
    # TIME MODE
    elif (modeSplit[1]=="-t"):
        for e in ROOT.findall("event"):
            if (e.get("time") == modeSplit[2]):
                ROOT.remove(e)
                TREE.write(PATH)
                print("Event removed.")
        
    # ERROR
    else:
        print("Wrong use of parameters/arguments! Use 'help' to have more info"+
        " about the use of the 'remove' function.")
    return
    
# PRETTY PRINT XML
def prettify():
    nonPrettyXML = MD.parse(PATH)
    prettyXML = nonPrettyXML.toprettyxml(indent="  ")
    # OPEN / WRITE / CLOSE
    toPrettify = open(PATH, "w")
    toPrettify.write(prettyXML)
    toPrettify.close()
    return

# CREATE .ICS FILE
def makeICS(event):
    ics = open(event.name + ".ics","w")
    ics.write("BEGIN:VCALENDAR\n")
    ics.write("VERSION:2.0\n")
    ics.write("CALSCALE:GREGORIAN\n")
    ics.write("BEGIN:VEVENT\n")
    ics.write("DTSTART:")
    ics.write(event.date.split("/")[2])
    ics.write(event.date.split("/")[1])
    ics.write(event.date.split("/")[0]+ "T")
    ics.write(event.time.split(":")[0])
    ics.write(event.time.split(":")[1] + "00\n")
    ics.write("DTEND:")
    ics.write(event.date.split("/")[2])
    ics.write(event.date.split("/")[1])
    ics.write(event.date.split("/")[0]+ "T")
    ics.write(event.time.split(":")[0])
    ics.write(event.time.split(":")[1] + "30\n")
    ics.write("UID:" + event.name + "\n")
    ics.write("SUMMARY:" + event.name + "\n")
    ics.write("LOCATION:" + event.place + "\n")
    ics.write("DESCRIPTION:" + event.desc + "\n")
    ics.write("PRIORITY:1\n")
    ics.write("END:VEVENT\n")
    ics.write("END:VCALENDAR\n")
    ics.close()
    ics = open(event.name + ".ics", "rb")
    # SEND AS MAIL ATTACHMENT
    sendMailWithAttachment(ics.read())
    ics.close()
    # DELETE THE FILE
    os.remove(event.name + ".ics")
    return

# EMAIL ATTACHMENT SELF SENDER
def sendMailWithAttachment(ics):
    # STRUCTURE MAIL
    msg = MIMEMultipart()
    msg['Subject'] = "Nuovo evento da aggiungere al calendario"
    msg['From'] = MAIL
    msg['To'] = MAIL

    # GENERATE ATTACHMENT
    x = MIMEBase('application', 'octet-stream')
    x.set_payload(ics)
    x.add_header('Content-Disposition', 'attachment; filename="file.ics"')
    msg.attach(x)

    # SEND EMAIL VIA SMTP GMAIL SERVER
    s = smtplib.SMTP(SMTP_SERVER)
    s.ehlo()
    s.starttls()
    s.login(LOGIN, PASSWORD)
    s.send_message(msg)
    s.quit()
    return

# CHECK FOR THE PASSED EVENTS, REMOVE THEM
def checkExpirated():
    erased = 0
    for e in ROOT.findall("event"):
        if (not e.get("date")):
          continue
        year = int(e.get("date").split("/")[2])
        month = int(e.get("date").split("/")[1])
        day = int(e.get("date").split("/")[0])
        hour = int(e.get("time").split(":")[0])
        minu = int(e.get("time").split(":")[1])
        if (not e.get("date")):
            continue
        elif (year<int(time.strftime("%Y"))):
            ROOT.remove(e)
            TREE.write(PATH)
            erased+=1

        elif (year==int(time.strftime("%Y"))):
            if (month<int(time.strftime("%m"))):
                ROOT.remove(e)
                TREE.write(PATH)
                erased+=1

            elif (month==int(time.strftime("%m"))):
                if (day<int(time.strftime("%d"))):
                    ROOT.remove(e)
                    TREE.write(PATH)
                    erased+=1

                elif (day==int(time.strftime("%d"))):
                    if (hour<int(time.strftime("%H"))):
                        ROOT.remove(e)
                        TREE.write(PATH)
                        erased+=1

                    elif (hour==int(time.strftime("%H"))):
                        if (minu<int(time.strftime("%M"))):
                            ROOT.remove(e)
                            TREE.write(PATH)
                            erased+=1

        else:
            continue
    if (erased > 0):
        print(str(erased) + " events were past events and were removed.")
    return


# EXECUTION CODE

if (len(sys.argv)==1):
    checkExpirated()
    inpLine()
else :
    print("Error.")
    print("Wrong number of arguments! Use only defschedule.")
