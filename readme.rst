************************
Monospace font condenser
************************

A script to horizontally condense monospaced fonts so that you can have more
text in each line (or shorter lines) and read more letters with each eye fixation.

It just makes most good monospaced font even better for programming or terminal
usage by:
 
 1. removing horizontal space between glyphs
 2. shrinking the glyph horizontally

Mandatory screenshot:

.. image:: https://raw.github.com/soulrebel/fontcondenser/master/screenshot.png


Usage example
+++++++++++++

I suggest to clone the repository directly in your ~/.fonts, than use from
there:

``./condense.sh <xratio> <xclip> <font> [additional fonts]``

for example to condense the Ubuntu Mono font, in all its variants, to 90% and
clipping 4 font units use:

``./condense.sh .90 -4 /usr/share/fonts/TTF/UbuntuMono-*``

Good free fonts that can use some condensing are: 

 * Ubuntu Mono
 * Droid Sans Mono
 * Liberation Mono
 * Anonymous Pro

Requirements
++++++++++++

 * python 2
 * fontforge and its python bindings

Project files
+++++++++++++

 * condense.sh the script to condense many fonts in batch
 * condense_single.py the python code to condense a single font file

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

TODO
++++

 * validate parameters
 * calculate bounding box and reduce intra-font spacing automatically
 * upscale the condensed font to compensate
 * add links and details in documentation

