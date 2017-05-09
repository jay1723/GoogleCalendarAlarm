from __future__ import print_function
import httplib2
import os
import sys
import pygame
from pygame import mixer

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from datetime import timedelta
from dateutil import parser

# GOOGLE CALENDAR AUTHENTICATION/Retrieval
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

# Playing media files
def playFile(fileName):
    pygame.mixer.pre_init(22050, -16, 2, 4096)
    pygame.init()
    pygame.mixer.music.load(fileName)
    pygame.mixer.music.play(1)

# While there is playback don't exit the method
    while pygame.mixer.music.get_busy:
        continue

# Checks the timing for the events
def checkTiming(cYear, cMonth, cDay, cHour, cMinute, eYear, eMonth, eDay, eHour, eMinute):
    # Checks the Year, Month, Day, and Hour are equal.
    if (cYear == eYear and cMonth == eMonth and cDay == eDay and cHour == eHour):
        # Case where the event timer happens from 1-59
        if (eMinute - 1  == cMinute):
            return True
        elif (eMinute == 0 and cMinute == 59):
            return True
    # Case where the dates don't match
    return False

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """

    # Boilerplate authentication code provided by GOOGLE
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #minute = timedelta(minutes = 1)
    #maxTime = (datetime.datetime.utcnow() + minute).isoformat() + 'Z'
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    # pygame.mixer.init()
    # pygame.mixer.music.load('/Users/Jay1723/Documents/Songs/TujhMeinRabDikhtaHai.mp3')
    # pygame.mixer.music.play()

    if not events:
        print('No upcoming events found.')
    for event in events:
        #test = event['start'].get('dateTime')

        # Start information for the event
        fullTime = parser.parse(event['start'].get('dateTime'))
        startYear = fullTime.year
        startMonth = fullTime.month
        startDay = fullTime.day
        startHour = fullTime.hour
        startMinute = fullTime.minute

        # Current time information
        currentTime = datetime.datetime.now()
        currentYear = currentTime.year
        currentMonth = currentTime.month
        currentDay = currentTime.day
        currentHour = currentTime.hour
        currentMinute = currentTime.minute
        currentSecond = currentTime.second

        WakeUpList = ['Wake up', 'wake up', 'Wake Up']
        LeaveList = ['Leave for work', 'Leave For Work', 'leave for work']
        OtherList = ['Other tasks', 'Other Tasks', 'other tasks', 'Other task', 'Other Task', 'other task']
        GoUpstairList = ['Go Upstairs', 'Go upstairs', 'go upstairs']
        LightsOutList = ['Lights Out', 'Lights out', 'lights out']

        # Checks the summary of the event and the time stamp of the event

        # Wake Up
        if event.get('summary') in WakeUpList:
            if(checkTiming(currentYear, currentMonth, currentDay, currentHour, currentMinute, startYear, startMonth, startDay, startHour, startMinute)):
                playFile('/home/pi/AlarmClock/Reveille.mp3')

        # Leave for Work
        if event.get('summary') in LeaveList':
            if(checkTiming(currentYear, currentMonth, currentDay, currentHour, currentMinute, startYear, startMonth, startDay, startHour, startMinute)):
                playFile('/home/pi/AlarmClock/ToTheColor.mp3')

        # Other Tasks
        if event.get('summary') in OtherList:
            if(checkTiming(currentYear, currentMonth, currentDay, currentHour, currentMinute, startYear, startMonth, startDay, startHour, startMinute)):
                playFile('/home/pi/AlarmClock/MessCall.mp3')

        # Go Upstairs
        if event.get('summary') in GoUpstairList:
            if(checkTiming(currentYear, currentMonth, currentDay, currentHour, currentMinute, startYear, startMonth, startDay, startHour, startMinute)):
                playFile('/home/pi/AlarmClock/CallToQuarters.mp3')

        # Lights Out
        if event.get('summary') in LightsOutList:
            if(checkTiming(currentYear, currentMonth, currentDay, currentHour, currentMinute, startYear, startMonth, startDay, startHour, startMinute)):
                playFile('/home/pi/AlarmClock/Taps.mp3')

if __name__ == '__main__':
    main()
