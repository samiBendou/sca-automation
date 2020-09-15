"""Export and plot data from SoC.

The data retrieved from SoC consists on side-channel leakage
and encryption data in order to later perform correlation.

The side-channel leakage is plot to evaluate the quality of
the acquisition.
The data is exported in 3 separated CSV files.

Examples
--------
.. code-block:: shell

    $ python acquire.py 256 COM5
    $ python acquire.py -m sw 1024 cmd

In the above example, the first line will launch the acquisition
of 256 hardware traces and read the serial port ``COM5``.

The second line will read the file ``cmd_hw_1024.log`` located in the
directory containing the 1024 software traces.

In the last case, the file must be a valid binary log file previously
acquired from the SoC via serial port.

"""

import argparse
import os

import numpy as np
import ui

from datetime import datetime
import ui.actions
import ui.update
import ui.plot
from lib import data
from lib.data import Request
from lib import traces as tr
from scipy import fft, signal


@ui.actions.timed("acquire.py", "\nexiting...")
def main(args):
    f_nyq = 200e6 / 2
    order = 4
    w = 13e6 / f_nyq
    b0, a0, *_ = signal.butter(order, w, btype="highpass", output="ba")

    w0 = 49e6 / f_nyq
    w1 = 51e6 / f_nyq
    b1, a1, *_ = signal.butter(order, [w0, w1], btype="bandstop", output="ba")

    @ui.actions.timed("start acquisition")
    def prepare(_, chunk=None):
        if chunk is not None:
            print(f"{'chunk':<16}{chunk + 1}/{args.chunks}")
            print(f"{'requested':<16}{(chunk + 1) * request.iterations}/{request.iterations * request.chunks}")
        print(f"{'started':<16}{datetime.now():%Y-%m-%d %H:%M:%S}")

    @ui.actions.timed("start processing", "\nprocessing successful!")
    def process(x, chunk=None):
        print(f"{'started':<16}{datetime.now():%Y-%m-%d %H:%M:%S}")
        parser = data.Parser(x, direction=request.direction, verbose=request.verbose)
        ui.save(request, x, parser.leak, parser.channel, parser.meta, parser.noise, chunk=chunk, path=savepath)
        print(f"{'size':<16}{ui.sizeof(len(x or []))}")
        print(f"{'parsed':<16}{len(parser.channel)}/{request.iterations}")

        traces = np.array(tr.adjust(parser.leak.traces, trace))
        mean = ui.update.trace(trace, traces) / ((chunk if chunk else 0 + 1) * request.iterations)
        mean = signal.filtfilt(b0, a0, mean)
        mean = signal.filtfilt(b1, a1, mean)
        spectrum = np.absolute(fft.fft(mean))
        ui.plot.acquisition(traces, mean, spectrum, parser.meta, request, path=savepath)

    request = Request(args)
    savepath, loadpath = ui.actions.init(request, args.path)
    trace = None
    print(request)
    print(f"{'load path':<16}{os.path.abspath(loadpath)}")
    print(f"{'save path':<16}{os.path.abspath(savepath)}")
    ui.actions.acquire(request, process, prepare=prepare, path=loadpath)


argp = argparse.ArgumentParser(
    description="Acquire data from SoC and export it.")
argp.add_argument("iterations", type=int,
                  help="Requested count of traces.")
argp.add_argument("name", type=str,
                  help="Acquisition source name.")
argp.add_argument("-m", "--mode",
                  choices=[Request.Modes.HARDWARE, Request.Modes.SOFTWARE],
                  default=Request.Modes.HARDWARE,
                  help="Encryption mode.")
argp.add_argument("-d", "--direction",
                  choices=[Request.Directions.ENCRYPT, Request.Directions.DECRYPT],
                  default=Request.Directions.ENCRYPT,
                  help="Encryption direction.")
argp.add_argument("--chunks", type=int, default=None,
                  help="Count of chunks to acquire.")
argp.add_argument("--path", type=str, default=ui.actions.DEFAULT_DATA_PATH,
                  help="Path where to save files.")
argp.add_argument("-s", "--source",
                  choices=[Request.Sources.FILE, Request.Sources.SERIAL],
                  default=Request.Sources.FILE,
                  help="Acquisition source.")
argp.add_argument("-p", "--plot", type=int, default=16,
                  help="Count of raw traces to plot.")
argp.add_argument("--start", type=int,
                  help="Start time sample index of each trace.")
argp.add_argument("--end", type=int,
                  help="End time sample index of each trace.")
argp.add_argument("-v", "--verbose", action="store_true",
                  help="End time sample index of each trace.")

if __name__ == "__main__":
    main(argp.parse_args())
