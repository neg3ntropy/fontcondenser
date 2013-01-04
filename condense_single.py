#!/usr/bin/env python2

# Script to horizontally condense a single font font using fontforge
#
###############################################################################
# Copyright (C) 2013 Andrea Ratto <andrearatto at yahoo dot it> and
# contributors: (none so far)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
###############################################################################

import fontforge
import os
import psMat
import sys

xratio = float(sys.argv[1])
xmargin = int(sys.argv[2])
inputFont = sys.argv[3]

#example values
#inputFont = "DroidSansMono.ttf"
#xmargin=-16
#xratio=0.9

print "opening font:", inputFont
font = fontforge.open(inputFont)

orig_width = None
new_width = None
errors = []

for x in font:
    g = font[x]
    if (orig_width is None):
        orig_width = g.width
    
    if (g.width == orig_width): 
      g.transform(psMat.translate(-xmargin, 0))
      g.width = orig_width
      g.transform(psMat.translate(2 * xmargin, 0))
      g.transform(psMat.scale(xratio, 1))
    #else:
        #print "skipping " + x

for x in font:
    g = font[x]
    if (new_width is None):
        new_width = g.width
    
    if (g.width > 0 and new_width != g.width):
        errors.append("font is not monospaced, glyph %s has width %d instead of %d" % (x, g.width, new_width))

if (errors):
    for error in errors:
        print sys.stderr, error
    print >> sys.stderr, "errors found exiting"
    sys.exit(1)

# clipping the bottom can improve readability in some cases...
#font.descent += 2*xmargin

def rename(name, sep, suffix):
    n = name.split(sep,1)
    n[- min(2, len(n))] += suffix
    return sep.join(n)

font.sfnt_names = () # reset extra metadata

font.fontname = rename(font.fontname, '-', "Condensed") 
font.familyname = font.familyname + " Condensed" 
font.fullname = font.fullname + " Condensed"

outputFont = "condensed_%s.ttf" % (os.path.splitext(os.path.basename(inputFont))[0])
font.generate(outputFont)
print "saved %s (width: %d -> %d)" % (font.fontname, orig_width, g.width)
sys.exit(0)

