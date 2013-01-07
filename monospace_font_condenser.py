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

    @classmethod
    def make_relevant_subset(cls):
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
        relevant_chars = relevant_chars.replace('W','')
        relevant_chars = relevant_chars.replace('w','')
        relevant_subset = [fontforge.nameFromUnicode(ord(c)) for c in relevant_chars]
        return relevant_subset


    def __init__(self, input_file):
        "open the font in input_file for transformations"
        self.font = fontforge.open(input_file)
        self.input_file = input_file

    def condense(self, xratio, xclip):
        """
        processes the font first scaling it horizontally to xratio and then
        clipping extra whitespace between glyphs to xspacing_ratio.
        """
        orig_width = self._get_width()
        if xclip > 0:
            print "clipping %d points" % xclip   
            self.trim_spacing(xclip)
                
        self.horiz_condense(xratio)
        print "condensed from %d to %d" % (orig_width, self._get_width())

    def _get_width(self):
        """
        gets the width of a monospace font checking that all glyphs are
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


    def _get_min_horiz_bearing(self, width=None, sym_subset=None):
        """
        gets the minimun horizontal bearing found in all glyphs of the font
        argument. The bearing is the white space surrounding a glyph. 
        """ 
        if width is None:
            width = self._get_width()
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

    def scale(self, ratio, orig_width=None):
        "scale vertically and horizontally to the same ratio"
        if orig_width is None:
            orig_width = self._get_width()
        if ratio != 1:
            for sym in self.font:
                glyph = self.font[sym]
                if glyph.width == orig_width: 
                    glyph.transform(psMat.scale(ratio, ratio))

            
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

    def is_italic(self):
        return self.font.italicangle != 0

if __name__ == '__main__':
    
    relevant_subset = MonospaceFontCondenser.make_relevant_subset()
    print "considering %d relevant symbols" % len(relevant_subset)

    def find_xclip(xspacing_ratio, condensers):
        min_bearing = sys.maxint
        for condenser in condensers:
            if not condenser.is_italic():
                bearing = condenser._get_min_horiz_bearing(sym_subset=relevant_subset)
                min_bearing = min(bearing, min_bearing)
                if bearing == 0:
                    print >> sys.stderr, "Warning at least one glyph uses all the width," \
                            + " cannot reduce whitespace"
                    break
            else:
                print "skipping italic font"    
               
        xclip = int(math.ceil(min_bearing - xspacing_ratio * min_bearing))
        return xclip

    if len(sys.argv) < 4:
        usage = \
"""
Usage: 
%s <ratio> <spacing ratio> <horiz ratio> <fonts ...>

arguments
    ratio         scale everything to this ratio
    spacing ratio scale gratuitous white space between letters to this ratio
    horiz ratio   scale horizontally to this ratio
    font          one or more paths to the font files that make up a font family

example:
    enlarge all Ubuntu Mono fonts variants 15%%, then cut spacing to 30%%,
    then condense horizontally to 85%%

    %s 1.15 .3 .85 /usr/share/fonts/TTF/UbuntuMono-*
""" % (sys.argv[0], sys.argv[0])

        print >> sys.stderr, usage         
        sys.exit(1)

    ratio = float(sys.argv[1])
    xspacing_ratio = float(sys.argv[2])
    xratio = float(sys.argv[3])

    total = len(sys.argv) - 4
    print "%d fonts to process" % total
    
    errors = []

    condensers = []
    for input_file in sys.argv[4:]:
        print "opening font:", input_file
        condensers.append(MonospaceFontCondenser(input_file))

    xclip = find_xclip(xspacing_ratio, condensers)
    print "clipping %d points of gratuitous spacing" % xclip

    for condenser in condensers:
        try:
            condenser.scale(ratio)
            condenser.condense(xratio, xclip)
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

