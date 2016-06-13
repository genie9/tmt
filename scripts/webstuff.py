#!/usr/bin/python

import webbrowser 
import sys


address = ' '.join(sys.argv[1:])

webbrowser.open('https://www.google.com/maps/place/' + address)


