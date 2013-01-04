#!/bin/bash
# example usage
# put in ~/.fonts and cd in there, then run:
# ./condense.sh .90 -4 /usr/share/fonts/TTF/UbuntuMono-*
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

dir="`dirname "$0"`"

xratio=$1
xclip=$2
shift 2

if [ -z "$@" ]; then
    echo "usage $0 <xratio> <xclip> <files>"
    exit 1
fi

exitcode=0
for x in "$@"; do 
    "$dir/condense_single.py" "$xratio" "$xclip" "$x"
    if [ $? -ne 0 ]; then
        exitcode=1 
    fi
done

if [ $exitcode -ne 0 ]; then
    echo "there where errors on some fonts" >&2
fi
exit $exitcode

