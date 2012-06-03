#!/bin/sh
# alternative: 
# wget -l 0 -r -A py -X .bzr,tests -nH 192.168.1.24:8000/

bzr pull
bzr clean-tree --force --unknown --ignored --detritus
