#!/usr/bin/python

# Import the needed libraries
import sys
import Texml.processor

# Input can be given by a path, output should be a file object
infile = 'latest/ad.tex.xml'
out    = file('out.tex', 'w')
# Older versions of python need the following code:
# out = open('out.tex', 'w')

# Parameters
width        = 75
encoding     = 'UTF-8'
always_ascii = 1
use_context  = latest/ad.tex.xml TeXML inside a try-except block
try:
  Texml.processor.process(
      in_stream    = infile,
      out_stream   = out,
      autonl_width = width,
      encoding     = encoding,
      always_ascii = always_ascii,
      use_context  = use_context)
except Exception, msg:
  print sys.stderr, 'texml: %s' % str(msg)

# Clean up resources
out.close()
