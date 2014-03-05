#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import struct
import time
import datetime
import os
import sys
from optparse import OptionParser


class ADC16Error(Exception):
    def __init__(self, message):
        self.msg = "ADC-16 Error: %s" % str(message)
    def __str__(self):
        return self.msg

class ADC16(object):
    def __init__(self, devfile):
        self.ser = serial.Serial(devfile,
                                 baudrate=9600,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_NONE,
                                 timeout=0,
                                 writeTimeout=1,
                                 stopbits=serial.STOPBITS_ONE)
        self.ser.setRTS(True)
        self.ser.setDTR(False)
        time.sleep(1)
        if self.ser == None: raise ADC16Error("open error")
        self.chs = [1, 2, 3, 4, 5, 6]

    def __del__(self):
        self.ser.close()
        del self

    def write(self, command):
        self.ser.write(chr(command))

    def read(self):
        x = self.ser.readline()
        x = struct.unpack('BBB', x)
        v = (x[1]*256 + x[2]) * 2.5/65536
        if x[0] == 45: v = -v
        return v

    def readclear(self):
        while len(self.ser.readline()) != 0: pass

    def get_voltage(self, ch=1):
        for i in range(1, 8):
            if ch == i: ch = 0x1F + 0x20*(ch - 1)
            pass
        self.readclear()
        self.write(ch)
        time.sleep(1)
        return self.read()

    def get_voltages(self, chlist=None):
        if chlist != None: self.chs = chlist
        ret =[]
        for i in self.chs: ret.append(self.get_voltage(i))
        return ret

    def get_current(self, ch=1):

        resistance = [2.4, 2.4, 2.4, 199.2, 199.6, 199.8] # Reference Resistor [Ohm]
        c = self.get_voltage(ch) / resistance[ch-1]
        return c
    
    def get_currents(self, chlist=None):
        if chlist != None: self.chs = chlist
        ret = []
        for i in self.chs: ret.append(self.get_current(i))
        return ret

if __name__ == '__main__':
    adc = ADC16('/dev/ttyUSB1')
    parser = OptionParser()
    parser.add_option(
        '-v', '--voltage',
        action='store_true',
        dest='v_flag',
        help='Getting Voltage value.'
        )
    # parser.add_option(
    #     '-f', '--filename',
    #     action='store',
    #     type='str',
    #     dest='filename'
    #     help='Set filename (e.g., foo.dat)'
    #     )
    options, args = parser.parse_args()

    if options.v_flag:
        print "# Time              Current [mV]"
    else:
        print "# Time              Current [mA]"
    print "# UTC+9  Unix Time  ch. 1  ch. 2  ch 3.  ch. 4  ch. 5  ch. 6"
    while True:
        try:
            ut = int(time.time())
            t = time.strftime("%Y-%m-%d-%H:%M:%S")
            if options.v_flag: data = adc.get_voltages()
            else: data = adc.get_currents()
            dataRound = []
            for d in data: dataRound.append(round(d*1000., 3))
            print t, ut, "%+3.2f  "*6 % tuple(dataRound[i] for i in range(len(dataRound)))
            sys.stdout.flush()
        except KeyboardInterrupt: break
