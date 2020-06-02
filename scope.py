#!/usr/bin/env python3

#
# Download data from a Rigol DS1052E oscilloscope and graph with matplotlib.
#
# Copyright (C) 2020, @hexdump
#
# Based on code by Ken Shirriff at http://righto.com/rigol, which was
# in turn based on code by Cibo Mahto at  http://www.cibomahto.com/20\
# 10/04/controlling-a-rigol-oscilloscope-using-linux-and-python/
#

import numpy
import matplotlib.pyplot as plot
import sys
import usbtmc

scope = usbtmc.Instrument(6833, 1416)    

# Grab the raw data from channel 1
scope.write(":STOP")

# Get the timescale
timescale = float(scope.ask(":TIM:SCAL?"))

# Get the timescale offset
timeoffset = float(scope.ask(":TIM:OFFS?"))
voltscale = float(scope.ask(':CHAN1:SCAL?'))

# And the voltage offset
voltoffset = float(scope.ask(":CHAN1:OFFS?"))

scope.write(":WAV:POIN:MODE NOR")
rawdata = scope.ask_raw(b":WAV:DATA? CHAN1", 9000)
#rawdata = scope.read_raw(9000)
data_size = len(rawdata)
sample_rate = scope.ask(':ACQ:SAMP?')
print('Data size:', data_size, "Sample rate:", sample_rate)

scope.write(":RUN")
scope.write(":KEY:FORCE")
scope.close()

data = numpy.frombuffer(rawdata, 'B')

# Walk through the data, and map it to actual voltages
# This mapping is from Cibo Mahto
# First invert the data
data = data * -1 + 255

# Now, we know from experimentation that the scope display range is actually
# 30-229.  So shift by 130 - the voltage offset in counts, then scale to
# get the actual voltage.
data = (data - 130.0 - voltoffset/voltscale*25) / 25 * voltscale

# Now, generate a time axis.
time = numpy.arange(-300.0/50*timescale, 300.0/50*timescale, timescale/50.0)
#time = numpy.linspace(timeoffset - 6 * timescale, timeoffset + 6 * timescale, num=len(data))

if (time.size > data.size):
    time = time[0:600:1]

if (time[599] < 1e-3):
    time = time * 1e6
    tUnit = "uS"
elif (time[599] < 1):
    time = time * 1e3
    tUnit = "mS"
else:
    tUnit = "S"

# Plot the data
plot.plot(time, data[10:])
plot.title("Oscilloscope Channel 1")
plot.ylabel("Voltage (V)")
plot.xlabel("Time (" + tUnit + ")")
plot.xlim(time[0], time[599])
plot.show()
