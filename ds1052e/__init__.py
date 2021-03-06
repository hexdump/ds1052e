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

import numpy as np
from usbtmc import Instrument

class DS1052E:
    def __init__(self):
        self.port = Instrument(6833, 1416)

    def stop(self):
        self.port.write(":STOP")

    def resume(self):
        self.port.write(":RUN")
        self.port.write(":KEY:FORCE")        
        
    def sample(self, channel="CHAN1", stop=True):
        if channel not in ["CHAN1", "CHAN2", "MATH"]:
            raise ValueError(".sample() channel must be one of: "
                             "\"CHAN1\", \"CHAN2\", \"MATH\"")

        # read parameters of observation
        timescale = float(self.port.ask(":TIM:SCAL?"))
        timeoffset = float(self.port.ask(":TIM:OFFS?"))
        voltscale = float(self.port.ask(f":{channel}:SCAL?"))
        voltoffset = float(self.port.ask(f":{channel}:OFFS?"))

        # load samples
        self.port.write(":WAV:POIN:MODE NOR")
        rawdata = self.port.ask_raw(b":WAV:DATA? " + channel.encode('utf-8'), 9000)

        # convert data from raw bytes and add a time axis
        data = np.frombuffer(rawdata, "B")
        data = data * -1 + 255
        data = (data - 130.0 - voltoffset/voltscale*25) / 25 * voltscale
        time = np.arange(-300.0/50*timescale, 300.0/50*timescale, timescale/50.0)

        return (time[50:600], data[50:600])
