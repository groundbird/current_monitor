#!/bin/sh

DATADIR=/home/gb/current_monitor/data
FILENAME=`date '+%Y%m%d%H%M%S'`
CMD=/home/gb/current_monitor/adc.py

${CMD} | tee ${DATADIR}/${FILENAME}.dat
