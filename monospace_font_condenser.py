#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :

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
import math

class MonospaceFontCondenser(object):
    "Condense monospace fonts"

    relevant_subset = None

    @classmethod
    def use_relevant_subset(cls):
        """
        A string of all characters to be used for finding the glyph spacing.
        Glyphs that are wider than those listed here can be shrunk a little more.
        
        For example a capital 'W' might have space around it, because a some rarely
        used symbol, like 'Æ' needs more room. If by shrinking those rarely used
        glyphs a little more, we can reduce spacing around most characters without
        shrinking them, it is considered worthwhile.
        """
   
        str_char_range = lambda start, end: \
                "".join([chr(x) for x in range(ord(start), ord(end) + 1)])

        ascii_lower = str_char_range('a','z')
        ascii_upper = str_char_range('A','Z')
        ascii_num = str_char_range('0','9')
        symbols = '$@(){}[]'
        unicode_extras = u""

        relevant_chars = u"" + ascii_lower + ascii_upper + ascii_num + symbols + \
                unicode_extras
        
        cls.relevant_subset = [fontforge.nameFromUnicode(ord(c)) for c in relevant_chars]


    def __init__(self, input_file):
        "Open the font in input_file for transformations"
        self.font = fontforge.open(input_file)
        self.input_file = input_file

    def condense(self, xratio, xspacing_ratio):
        """
        processes the font first scaling it horizontally to xratio and then
        scaling extra whitespace between glyphs to xspacing_ratio.

        For example condense(.80, 0) scales the font to 80% horizontally and
        clips all unnecessary white, so that the widest letters will touch.
        """
        orig_width = self._get_width()
        if xspacing_ratio < 1:
            max_xspacing = self._get_min_horiz_bearing(orig_width, self.relevant_subset)
            if max_xspacing == 0:
                print >> sys.stderr, "Warning at least one glyph uses all the width," \
                        + " cannot reduce whitespace"
            else:
                xclip = int(math.ceil(max_xspacing - xspacing_ratio * max_xspacing))
                print "clipping %d points of extra white space out of %d" % \
                        (xclip, max_xspacing)
                self.trim_spacing(xclip, orig_width)
                orig_width = self._get_width()
                
        self.horiz_condense(xratio, orig_width)
        print "condensed from %d to %d" % (orig_width, self._get_width())

    def _get_width(self):
        """
        Gets the width of a monospace font checking that all glyphs are
        effectively of the same width.
        """
        font_width = None

        for sym in self.font:
            glyph = self.font[sym]
            width = glyph.width
            if width > 0:
                # tolerate empty glyphs
                if font_width is None:
                    font_width = width
                elif font_width != width:
                    raise ValueError('font is not monospaced: ' +
                            'glyph %s has width %d instead of expected %d'
                            % (sym, width, font_width))
        return font_width


    def _get_min_horiz_bearing(self, width, sym_subset=None):
        """
        Gets the minimun horizontal bearing found in all glyphs of the font
        argument. The bearing is the white space surrounding a glyph. 
        """ 
        min_bearing = sys.maxint
        min_bearing_sym = None
        for sym in sym_subset or self.font:
            glyph = self.font[sym]
            bbox = glyph.boundingBox()
            if glyph.width > 0 and (bbox[1] != 0 or bbox[3] != 0):
                lbearing = bbox[0]
                rbearing = width - bbox[2]
                glyph_min_bearing = min(lbearing, rbearing)
                if glyph_min_bearing < min_bearing:
                    min_bearing_sym = sym
                    if glyph_min_bearing <= 0:
                        min_bearing = 0
                    else:
                        min_bearing = glyph_min_bearing
        print "minimum bearing of %d found at %s" % (min_bearing, min_bearing_sym)
        return min_bearing


    def horiz_condense(self, xratio, orig_width=None):
        "condense the font horizontally to the given xratio"
        if orig_width is None:
            orig_width = self._get_width()
        if xratio != 1:
            for sym in self.font:
                glyph = self.font[sym]

                if glyph.width == orig_width: 
                    glyph.transform(psMat.scale(xratio, 1))

    def upscale(self, ratio, orig_width=None):
        "condense the font horizontally to the given xratio"
        if orig_width is None:
            orig_width = self._get_width()
        if xratio != 1:
            for sym in self.font:
                glyph = self.font[sym]

                if glyph.width == orig_width: 
                    glyph.transform(psMat.scale(ratio))

    def trim_spacing(self, xtrim, orig_width=None):
        "trims xtrim points around each glyph of font"
        if orig_width is None:
            orig_width = self._get_width()
        for sym in self.font:
            glyph = self.font[sym]
            if glyph.width == orig_width:
                rbearing = int(math.floor(max(0, glyph.right_side_bearing)))
                lbearing = int(math.floor(max(0, glyph.left_side_bearing)))
                if lbearing + rbearing == orig_width:
                    glyph.width = orig_width - 2 * xtrim
                else:
                    glyph_trim = min(xtrim, lbearing, rbearing)
                    glyph.transform(psMat.translate(glyph_trim, 0))
                    glyph.width = orig_width
                    glyph.transform(psMat.translate(-2 * glyph_trim, 0))

                    glyph_width = glyph.width
                    to_shrink = 2 * (xtrim - glyph_trim)

                    if to_shrink > 0:
                        print "%d out of %d points could not be trimmed on %s, scaling" \
                                % (to_shrink/2, xtrim, sym)
                        xratio = float(glyph_width - to_shrink)/ glyph_width
                        glyph.transform(psMat.scale(xratio, 1))

    def vert_stretch(self, yratio):
        pass

    @staticmethod
    def _rename(name, sep, suffix):
        n = name.split(sep,1)
        n[- min(2, len(n))] += suffix
        return sep.join(n)

    def update_font_name(self, suffix='condensed'):
        "appends suffix to the font name metadata"
        font = self.font
        font.sfnt_names = () # reset extra metadata
        font.fontname = self._rename(font.fontname, '-', suffix) 
        font.familyname = font.familyname + " " + suffix 
        font.fullname = font.fullname + " " + suffix

    def save(self, path='.', output_fmt='condensed_%s.ttf'):
        outputfont = output_fmt % (os.path.splitext(
            os.path.basename(self.input_file))[0])
        self.font.generate(os.path.join(path, outputfont))


if __name__ == '__main__':
    
    MonospaceFontCondenser.use_relevant_subset()
    
    if len(sys.argv) < 4:
        usage = \
"""
Usage: 
%s <horiz ratio> <spacing ratio> <scale ratio> <fonts ...>

arguments
    horiz ratio    scale horizontally to this ratio
    spacing ratio  scale gratuitous white space between letters to this ratio
    scale ratio    scale everything to this ratio
    font           one or more paths to a font file

example:
    scale all Ubuntu Mono fonts variants horizontally 85%%, cut spacing in half,
    then enlarge 10%%

    %s .90 .5 1.1 /usr/share/fonts/TTF/UbuntuMono-*
""" % (sys.argv[0], sys.argv[0])

        print >> sys.stderr, usage         
        sys.exit(1)

    xratio = float(sys.argv[1])
    xspacing_ratio = float(sys.argv[2])
    upscale_ratio = float(sys.argv[3])

    total = len(sys.argv) - 4
    print "%d fonts to process" % total
    
    errors = []

    for input_file in sys.argv[4:]:
        try:
            print "opening font:", input_file
            condenser = MonospaceFontCondenser(input_file)
            condenser.condense(xratio, xspacing_ratio)
            condenser.upscale(upscale_ratio)
            condenser.update_font_name()
            condenser.save()
            print "font saved"

        except Exception as e:
            import traceback
            traceback.print_exc()
            print "failed"
            errors.append("condensing font %s failed: %s" 
                    % (input_file, e.message))

    exitcode = 0
    
    for error in errors:
        print >> sys.stderr, "Error:", error
        exitcode = 1

    print "%d font(s) processed succesfully out of %d" % \
            (total - len(errors), total)
    sys.exit(exitcode)

