# TSC (Terminal Script Collection)
A set of Python scripts for CLI use (or conky!), doing some boring automation.

# Requisites:
The pip3 Colored library is needed.
Install it with:
`pip3 install colored` 

# The scripts
Put this stuff where you like! In your .bashrc, or in your conky configuration files, use them whenever and wherever you like!
- __defnotes__ is a CLI interface to write down events or notes in an json file and access them via __monthlynotes__ which displays the list of events occurring in a certain month, and automatically deletes past events.
- __streamers__ is a terminal utility (most useful in conky!) that prints the current status (Online/Offline) of your favourite Twitch streamers.
- __schedule__ is a terminal utility which shows the daily schedule along with birthdays and festivities (needs some rework for use in conky).

# Configuration
Open the scripts and set up your stuff!

- __defnotes__ needs a PATH for the .json file.
- __streamers__ needs your Twitch username and the ID of your Twitch API (just register on the Twitch API website).
- __schedule__ needs a PATH for the .json file.


