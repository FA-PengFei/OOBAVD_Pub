#!/bin/bash

#dir=/home/pi/oobavd

cd /home/pi/oobavd/raw_gadget
bash ./insmod.sh #thanks gab 
cd /home/pi/oobavd
python /home/pi/oobavd/oobavd.py 
