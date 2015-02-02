#!/bin/sh

CURRDIR=`pwd`
DATADIR="${CURRDIR}/data"
FILENAME=`date '+%Y%m%d%H%M%S'`
CMD=${CURRDIR}/adc.py

if [ ! -d "${CURRDIR}/data" ]; then
    mkdir data
    echo 'Make data/'
fi

${CMD} | tee ${DATADIR}/${FILENAME}.dat
