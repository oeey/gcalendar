#!/usr/bin/env python

# modified from:
# https://developers.google.com/api-client-library/python/samples/authorized_api_cmd_line_calendar.py

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


if __name__ == '__main__':
    main()
