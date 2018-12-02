#!/usr/bin/python3
'''
Merutochan
http://merutochan.it
'''
import requests
import urllib.request

# Client ID and name
CLIENT_ID = 'YOUR_CLIENT_ID'
USER = 'YOUR_USER'
streamers = []
# Prepare header of requests
headers= {'Client-ID':CLIENT_ID}
# Check internet connection first
try:
  urllib.request.urlopen("http://www.twitch.tv")
except urllib.error.URLError as e:
  print("No internet connection.")
  exit()
  
# Get list of user followed channels through Kraken API
r = requests.get("https://api.twitch.tv/kraken/users/"+USER+"/follows/channels", headers=headers)
for s in r.json()['follows']:
	streamers.append( [ s['channel']['name'], str(s['channel']['_id']) ] )

# Check streamers status through Helix API
for s in streamers:
  r = requests.get("https://api.twitch.tv/helix/streams?user_id="+s[1], headers=headers)
  if r.json()['data']:
    print("$color0 "+s[0]+" online.")
  else:
    print("$color1 "+s[0]+" offline.")
