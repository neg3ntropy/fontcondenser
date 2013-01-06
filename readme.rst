************************
Monospace font condenser
************************

A script to horizontally condense monospaced fonts so that you can have more
text in each line (or shorter lines) and read more letters with each eye fixation.

It just makes most good monospaced font even better for programming or terminal
usage by:
 
 1. removing gratuitous horizontal space between glyphs, if present
 2. shrinking the glyphs horizontally
 3. enlarging glyphs but keeping the line height the same

Mandatory screenshot:

.. image:: https://raw.github.com/soulrebel/fontcondenser/master/screenshot.png

What does it mean gratuitous white space? If all relevant letters are actually
smaller than the allocated width, we have some gratuitous white space, that can
be slashed hard, without making the glyphs themselves harder to read.

Usage example
+++++++++++++

I suggest to clone the repository directly in your ~/.fonts, than use from
there:

``./monospace_font_condenser.py <horiz ratio> <spacing ratio> <scale ratio> <fonts ...>``

arguments:

    horiz ratio    scale horizontally to this ratio
    spacing ratio  scale gratuitous white space between letters to this ratio
    scale ratio    scale everything to this ratio
    font           one or more paths to a font file

for example to condense all Ubuntu Mono fonts variants horizontally to 85%, cut
spacing in half, then enlarge 10%:

``./monospace_font_condenser.py .85 .3 1.15 /usr/share/fonts/TTF/UbuntuMono-*``

Good free fonts that can use some condensing are: 

 * Ubuntu Mono
 * Droid Sans Mono
 * Liberation Mono
 * Anonymous Pro

Requirements
++++++++++++

 * python 2
 * fontforge and its python bindings

License
+++++++

Copyright (C) 2013 Andrea Ratto <andrearatto at yahoo dot it> and
contributors: (none so far)

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Credits
+++++++

Originally written by `Andrea Ratto <mailto:andrearatto at yahoo dot it>`_,
inspired by `Cay Hortsmann
<http://weblogs.java.net/blog/cayhorstmann/archive/2010/11/22/condensed-monospaced-font>`_.

