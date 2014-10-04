#!/usr/bin/env python

# modified from:
# https://developers.google.com/api-client-library/python/samples/authorized_api_cmd_line_calendar.py

import httplib2
import sys
import time
import datetime

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets


def main():

    scope = 'https://www.googleapis.com/auth/calendar'
    flow = flow_from_clientsecrets('client_secret.json', scope=scope)

    storage = Storage('credentials.dat')
    credentials = storage.get()

    class fakeargparse(object):  # fake argparse.Namespace
        noauth_local_webserver = True
        logging_level = "ERROR"
    flags = fakeargparse()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, flags)

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)

    # get the next 12 hours of events
    epoch_time = time.time()
    start_time = epoch_time - 3600  # 1 hour ago
    end_time = epoch_time + 12 * 3600  # 12 hours in the future
    tz_offset = - time.altzone / 3600
    if tz_offset < 0:
        tz_offset_str = "-%02d00" % abs(tz_offset)
    else:
        tz_offset_str = "+%02d00" % abs(tz_offset)
    start_time = datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%dT%H:%M:%S") + tz_offset_str
    end_time = datetime.datetime.fromtimestamp(end_time).strftime("%Y-%m-%dT%H:%M:%S") + tz_offset_str
    print "Getting calendar events between: " + start_time + " and " + end_time

    events = service.events().list(calendarId='primary', timeMin=start_time, timeMax=end_time, singleEvents=True).execute()
    #pprint.pprint(events)
    for event in events['items']:
        print event["summary"]

if __name__ == '__main__':
    main()

