#!/bin/bash
pip3 install requests validators
echo '<title>{$3rv3r_$!d3_fa!lur3}</title>' > /opt/index.html
python3 -m http.server 8080 --directory /opt/ &
/usr/bin/python3 /challenge/core.py 9002