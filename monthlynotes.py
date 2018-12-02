PATH = "PATH/events.xml"
"""
Merutochan
http://merutochan.it

"""
# LIBRARIES
import xml.etree.ElementTree as ET
import colored
import time

# XML File
TREE = ET.parse(PATH)
# Get root of XML file
ROOT = TREE.getroot()
# COLORS
color = colored.fg(226)
color2 = colored.fg(120)
color3 = colored.fg(87)
color4 = colored.fg(82)
color5 = colored.fg(5)
r = colored.attr('reset')

# CHECK PASSED EVENTS
def check_passed():
    erased = 0
    for e in ROOT.findall("event"):
        if (not e.get("date")):
          continue
        year = int(e.get("date").split("/")[2])
        month = int(e.get("date").split("/")[1])
        day = int(e.get("date").split("/")[0])
        hour = int(e.get("time").split(":")[0])
        minu = int(e.get("time").split(":")[1])
        
        if (year<int(time.strftime("%Y"))):
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
        print(str(erased) + " past events removed.")
    return

# EXECUTION CODE

check_passed()
for e in ROOT.findall("event"):
    # SHOW THE EVENTS OF THE SAME MONTH
    if(not e.get("date")):
        print(color5+e.get("name")+r)
        print(color3+e.get("desc")+r)
        print()
    elif(e.get("date").split("/")[1] == time.strftime("%m")):
        print(color5+e.get('name')+r)
        print(color+"["+e.get("date")+"] "+r+color2+"("+e.get("time")+") "+r+
        color3+e.get("desc")+r+color4+" @ ["+e.get("place")+"]"+r)
        print()