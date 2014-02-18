#!/bin/sh

DATADIR=/home/gb/adc16/data
FILENAME=`date '+%Y%m%d%H%M%S'`
CMD=/home/gb/adc16/adc.py

${CMD} | tee ${DATADIR}/${FILENAME}.dat
