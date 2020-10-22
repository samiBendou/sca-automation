import os
from enum import Enum
from tkinter import *
from tkinter import ttk

import serial.tools.list_ports

from lib.data import Request


def _set_validation_fg(widget, valid, optional=False, value=None):
    if not optional:
        widget.config({"foreground": "Green" if valid else "Red"})
        return

    if valid and not value:
        widget.config({"foreground": "Black"})
    else:
        widget.config({"foreground": "Green" if valid else "Red"})


class GeneralFrame(LabelFrame):
    class Mode(Enum):
        HARDWARE = "Hardware"
        TINY = "Tiny"
        SSL = "OpenSSL"
        DHUERTAS = "Dhuertas"

    MODE_POS = {name.value: i for i, name in enumerate(Mode)}

    class Model(Enum):
        SBOX = "SBox R0"
        INV_SBOX = "InvSBox R10"

    MODEL_POS = {name.value: i for i, name in enumerate(Model)}

    def __init__(self, master):
        super().__init__(master, text="General")

        self._iterations = None
        self._mode = None
        self._model = None
        self._chunks = None
        self._target = None

        self.var_iterations = StringVar()
        self.var_target = StringVar()
        self.var_mode = StringVar()
        self.var_model = StringVar()
        self.var_chunks = StringVar()

        self.label_iterations = Label(self, text="Iterations *")
        self.label_iterations.grid(row=0, column=0, sticky=W, padx=4)
        self.entry_iterations = Entry(self, textvariable=self.var_iterations)
        self.entry_iterations.grid(row=0, column=1, sticky=EW, padx=4)

        self.label_chunks = Label(self, text="Chunks")
        self.label_chunks.grid(row=1, column=0, sticky=W, padx=4)
        self.entry_chunks = Entry(self, textvariable=self.var_chunks)
        self.entry_chunks.grid(row=1, column=1, sticky=EW, padx=4)

        self.label_mode = Label(self, text="Mode *")
        self.label_mode.grid(row=2, column=0, sticky=W, padx=4)
        self.box_mode = ttk.Combobox(self, values=[e.value for e in GeneralFrame.Mode], textvariable=self.var_mode)
        self.box_mode.grid(row=2, column=1, sticky=EW, padx=4)

        self.label_model = Label(self, text="Model *")
        self.label_model.grid(row=3, column=0, sticky=W, padx=4)
        self.box_model = ttk.Combobox(self, values=[e.value for e in GeneralFrame.Model], textvariable=self.var_model)
        self.box_model.grid(row=3, column=1, sticky=EW, padx=4)

        Grid.columnconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, iterations):
        if iterations is None:
            return
        self._iterations = iterations
        self.var_iterations.set(iterations)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode is None:
            return
        self._mode = mode
        self.var_mode.set(mode)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        if model is None:
            return
        self._model = model
        self.var_model.set(model)

    @property
    def chunks(self):
        return self._chunks

    @chunks.setter
    def chunks(self, chunks):
        if chunks is None:
            return
        self._chunks = chunks
        self.var_chunks.set(chunks)

    def _validate_iterations(self):
        iterations = None
        try:
            iterations = max(int(self.var_iterations.get()), 0)
            valid = iterations > 0
        except ValueError:
            valid = False

        self._iterations = iterations if valid else None
        _set_validation_fg(self.label_iterations, valid)
        return valid

    def _validate_mode(self):
        mode = self.var_mode.get()
        valid = mode in (m.value for m in GeneralFrame.Mode)
        self._mode = GeneralFrame.MODE_POS[mode] if valid else None
        _set_validation_fg(self.label_mode, valid)
        return valid

    def _validate_model(self):
        model = self.var_model.get()
        valid = model in (m.value for m in GeneralFrame.Model)
        self._model = GeneralFrame.MODEL_POS[model] if valid else None
        _set_validation_fg(self.label_model, valid)
        return valid

    def _validate_chunks(self):
        chunks = self.var_chunks.get()
        try:
            chunks = int(chunks)
            valid = chunks > 0
        except ValueError:
            valid = chunks == ""

        self._chunks = chunks if valid and chunks != "" else None
        _set_validation_fg(self.label_chunks, valid, optional=True, value=self._chunks)
        return valid

    def validate(self):
        valid = self._validate_mode()
        valid = self._validate_model() and valid
        valid = self._validate_chunks() and valid
        return self._validate_iterations() and valid

    def lock(self):
        self.entry_iterations["state"] = DISABLED
        self.entry_chunks["state"] = DISABLED
        self.box_mode["state"] = DISABLED
        self.box_model["state"] = DISABLED

    def unlock(self):
        self.entry_iterations["state"] = NORMAL
        self.entry_chunks["state"] = NORMAL
        self.box_mode["state"] = NORMAL
        self.box_model["state"] = NORMAL


class TargetFrame(LabelFrame):
    class Source(Enum):
        SERIAL = "Serial"
        FILE = "File"

    SOURCE_POS = {s.value: i for i, s in enumerate(Source)}

    def __init__(self, master):
        super().__init__(master, text="Target")
        Grid.columnconfigure(self, 2, weight=1)

        self._port = None
        self._path = None
        self._source = Request.Sources.FILE
        self.var_port = StringVar()
        self.var_path = StringVar()
        self.var_source = StringVar(value=self._source)
        self.var_infos = StringVar(value="Select a serial port...")
        self._devices = []
        self._descriptions = {}
        self._serial_numbers = {}

        self.radio_source_serial = Radiobutton(self,
                                               text="Serial",
                                               variable=self.var_source,
                                               value=Request.Sources.SERIAL)
        self.radio_source_serial.grid(row=0, column=0, sticky=W, padx=4)
        self.box_serial = ttk.Combobox(self, textvariable=self.var_port, values=[])
        self.box_serial.grid(row=0, column=1, sticky=NSEW, padx=4)
        self.label_infos = Label(self, textvariable=self.var_infos)
        self.label_infos.grid(row=0, column=2, sticky=NSEW, padx=8)

        self.radio_source_file = Radiobutton(self,
                                             text="Files",
                                             variable=self.var_source,
                                             value=Request.Sources.FILE)
        self.radio_source_file.grid(row=1, column=0, sticky=W, padx=4)
        self.entry_file = Entry(self, textvariable=self.var_path)
        self.entry_file.grid(row=1, column=1, sticky=NSEW, padx=4, columnspan=2)
        self.refresh()

    @property
    def target(self):
        return self._path if self._source == Request.Sources.FILE else self._port

    @target.setter
    def target(self, target):
        self.refresh()
        if target is None:
            return
        if target in self._devices:
            self.source = Request.Sources.SERIAL
            self.port = target
            return
        self.source = Request.Sources.FILE
        self.path = target

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        if port is None:
            return
        self._port = port
        self.var_port.set(port)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if path is None:
            return
        self._path = path
        self.var_path.set(path)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        if source is None:
            return
        self._source = source
        self.var_source.set(source)

    def refresh(self):
        ports = serial.tools.list_ports.comports()
        self._devices = [p.device for p in ports]
        self._descriptions = {p.device: p.usb_description() for p in ports}
        self._serial_numbers = {p.device: p.serial_number for p in ports}
        self.box_serial["values"] = self._devices

    def _validate_path(self):
        self._path = self.var_path.get()
        _set_validation_fg(self.radio_source_file, True)
        return True

    def _validate_port(self):
        port = self.var_port.get()
        valid = port in self._devices
        self._port = port if valid else None
        _set_validation_fg(self.radio_source_serial, valid)
        if valid:
            self.var_infos.set(f"{self._descriptions[self._port]} - {self._serial_numbers[self._port]}")
        else:
            self.var_infos.set("")
        return valid

    def validate(self):
        self._source = self.var_source.get()
        if self._source == Request.Sources.SERIAL:
            _set_validation_fg(self.radio_source_file, True, True, None)
            self.entry_file["state"] = DISABLED
            self.box_serial["state"] = NORMAL
            self.label_infos["state"] = NORMAL
            return self._validate_port()
        elif self._source == Request.Sources.FILE:
            _set_validation_fg(self.radio_source_serial, True, True, None)
            self.entry_file["state"] = NORMAL
            self.box_serial["state"] = DISABLED
            self.label_infos["state"] = DISABLED
            return self._validate_path()

    def lock(self):
        self.entry_file["state"] = DISABLED
        self.box_serial["state"] = DISABLED
        self.radio_source_serial["state"] = DISABLED
        self.radio_source_file["state"] = DISABLED
        self.label_infos["state"] = DISABLED

    def unlock(self):
        if self._source == Request.Sources.SERIAL:
            self.entry_file["state"] = DISABLED
            self.box_serial["state"] = NORMAL
        elif self._source == Request.Sources.FILE:
            self.entry_file["state"] = NORMAL
            self.box_serial["state"] = DISABLED

        self.radio_source_serial["state"] = NORMAL
        self.radio_source_file["state"] = NORMAL
        self.label_infos["state"] = NORMAL


class FilterFrame(LabelFrame):
    class Mode(Enum):
        AUTO = 0
        MANUAL = 1

    def __init__(self, master):
        super().__init__(master, text="Filter")
        self.var_mode = IntVar(value=0)
        self._mode = FilterFrame.Mode(value=0)
        self.radio_mode_auto = Radiobutton(self,
                                           text="Auto",
                                           variable=self.var_mode,
                                           value=FilterFrame.Mode.AUTO.value)
        self.radio_mode_auto.grid(row=0, column=0, sticky=W, padx=4)

        self.radio_mode_manual = Radiobutton(self,
                                             text="Manual",
                                             variable=self.var_mode,
                                             value=FilterFrame.Mode.MANUAL.value)
        self.radio_mode_manual.grid(row=1, column=0, sticky=W, padx=4)

    @property
    def mode(self):
        return self._mode

    def lock(self):
        self.radio_mode_auto["state"] = DISABLED
        self.radio_mode_manual["state"] = DISABLED

    def unlock(self):
        self.radio_mode_auto["state"] = NORMAL
        self.radio_mode_manual["state"] = NORMAL

    def validate(self):
        self._mode = FilterFrame.Mode(value=self.var_mode.get())
        return True


class FormatFrame(LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Format")

        self._start = None
        self._end = None
        self._chunks = None
        self._verbose = False
        self._noise = False
        self.var_end = StringVar()
        self.var_start = StringVar()
        self.var_chunks = StringVar()
        self.var_verbose = BooleanVar(value=self._verbose)
        self.var_noise = BooleanVar(value=self._noise)

        self.label_start = Label(self, text="Start")
        self.label_start.grid(row=0, column=0, sticky=W, padx=4)
        self.entry_start = Entry(self, textvariable=self.var_start)
        self.entry_start.grid(row=0, column=1, padx=4)

        self.label_end = Label(self, text="End")
        self.label_end.grid(row=1, column=0, sticky=W, padx=4)
        self.entry_end = Entry(self, textvariable=self.var_end)
        self.entry_end.grid(row=1, column=1, sticky=W, padx=4)

        self.label_verbose = Label(self, text="Verbose")
        self.label_verbose.grid(row=3, column=0, sticky=W, padx=4)
        self.check_verbose = Checkbutton(self,
                                         var=self.var_verbose,
                                         onvalue=True,
                                         offvalue=False)
        self.check_verbose.grid(row=3, column=1, padx=4)

        self.label_noise = Label(self, text="Noise")
        self.label_noise.grid(row=4, column=0, sticky=W, padx=4)
        self.check_noise = Checkbutton(self,
                                       var=self.var_noise,
                                       onvalue=True,
                                       offvalue=False)
        self.check_noise.grid(row=4, column=1, padx=4)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if start is None:
            return
        self._start = start
        self.var_start.set(start)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if end is None:
            return
        self._end = end
        self.var_end.set(end)

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        if verbose is None:
            return
        self._verbose = verbose
        self.var_verbose.set(verbose)

    @property
    def noise(self):
        return self._noise

    @noise.setter
    def noise(self, noise):
        if noise is None:
            return
        self._noise = noise
        self.var_noise.set(noise)

    def _validate_start(self):
        start = self.var_start.get()
        try:
            start = int(start)
            valid = 0 <= start <= (self._end or start)
        except ValueError:
            valid = start == ""

        self._start = start if valid and start != "" else None
        _set_validation_fg(self.label_start, valid, optional=True, value=self._start)
        return valid

    def _validate_end(self):
        end = self.var_end.get()
        try:
            end = int(end)
            valid = 0 <= (self._start or 0) <= end
        except ValueError:
            valid = end == ""

        self._end = end if valid and end != "" else None
        _set_validation_fg(self.label_end, valid, optional=True, value=self._end)
        return valid

    def validate(self):
        self._noise = self.var_noise.get()
        self._verbose = self.var_verbose.get()
        valid = self._validate_start()
        return self._validate_end() and valid

    def lock(self):
        self.entry_start["state"] = DISABLED
        self.entry_end["state"] = DISABLED
        self.check_verbose["state"] = DISABLED
        self.check_noise["state"] = DISABLED

    def unlock(self):
        self.entry_start["state"] = NORMAL
        self.entry_end["state"] = NORMAL
        self.check_verbose["state"] = NORMAL
        self.check_noise["state"] = NORMAL


class PerfsFrame(LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Performances")
        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        self.format = FormatFrame(self)
        self.format.grid(row=0, column=0, sticky=NSEW, padx=4)
        self.filter = FilterFrame(self)
        self.filter.grid(row=0, column=1, sticky=NSEW, padx=4)

    def lock(self):
        self.format.lock()
        self.filter.lock()

    def unlock(self):
        self.format.unlock()
        self.filter.unlock()

    def validate(self):
        valid = self.format.validate()
        return valid and self.filter.validate()


class FilesFrame(LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Exports")
        Grid.columnconfigure(self, 1, weight=1)
        self._path = os.path.abspath(os.sep.join(os.getcwd().split(os.sep)[:-1] + ["data"]))
        self.label_path = Label(self, text="Path *")
        self.label_path.grid(row=0, column=0, sticky=W, padx=4)
        self.var_path = StringVar(value=self._path)
        self.entry_path = Entry(self, textvariable=self.var_path)
        self.entry_path.grid(row=0, column=1, padx=4, sticky=EW)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if path is None:
            return
        self._path = path
        self.var_path.set(path)

    def _validate_path(self):
        path = self.var_path.get()
        valid = os.path.isdir(path) or os.path.isdir(os.sep.join(path.split(os.sep)[:-1]))
        self._path = path if valid else None
        _set_validation_fg(self.label_path, self._path)
        return valid

    def validate(self):
        return self._validate_path()

    def lock(self):
        self.entry_path["state"] = DISABLED

    def unlock(self):
        self.entry_path["state"] = NORMAL


class PlotFrame(LabelFrame):
    class Mode(Enum):
        STATISTICS = 0
        CORRELATION = 1
        NOISE = 2

    def __init__(self, master):
        super().__init__(master, text="Plots")
        self._mode = PlotFrame.Mode.CORRELATION
        self._old_mode = PlotFrame.Mode.CORRELATION
        self._byte = None
        self._old_byte = None
        self.var_mode = IntVar(value=self._mode.value)
        self.var_byte = StringVar(value=0)

        self.label_byte = Label(self, text="Byte")
        self.label_byte.grid(row=0, column=0, sticky=W, padx=4)
        self.entry_byte = Entry(self, textvariable=self.var_byte)
        self.entry_byte.grid(row=0, column=1, sticky=EW, padx=4)

        self.radio_mode_stats = Radiobutton(self,
                                            text="Statistics",
                                            variable=self.var_mode,
                                            value=PlotFrame.Mode.STATISTICS.value)
        self.radio_mode_stats.grid(row=1, column=0, sticky=W, padx=4)

        self.radio_mode_corr = Radiobutton(self,
                                           text="Correlation",
                                           variable=self.var_mode,
                                           value=PlotFrame.Mode.CORRELATION.value)
        self.radio_mode_corr.grid(row=2, column=0, sticky=W, padx=4)

        self.radio_mode_noise = Radiobutton(self,
                                            text="Noise",
                                            variable=self.var_mode,
                                            value=PlotFrame.Mode.NOISE.value)
        self.radio_mode_noise.grid(row=3, column=0, sticky=W, padx=4)

    def _validate_byte(self):
        byte = self.var_byte.get()
        try:
            byte = int(byte)
            valid = byte >= 0
        except ValueError:
            valid = byte == ""
            byte = 0
        if valid:
            self._old_byte = self._byte
            self._byte = byte
        else:
            self._byte = None
        _set_validation_fg(self.label_byte, valid, optional=True, value=self._byte)
        return valid

    @property
    def changed(self):
        return ((self._old_byte or 0) != (self._byte or 0)) or (self._old_mode != self._mode)

    @property
    def mode(self):
        return self._mode

    @property
    def byte(self):
        return self._byte

    def validate(self):
        self.on_click()
        return self._validate_byte()

    def on_click(self):
        self._old_mode = PlotFrame.Mode(value=self._mode.value)
        self._mode = PlotFrame.Mode(value=self.var_mode.get())


class ConfigFrame(LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Configuration")
        self.general = GeneralFrame(self)
        self.general.pack(side=TOP, expand=1, fill=BOTH)
        self.target = TargetFrame(self)
        self.target.pack(side=TOP, expand=1, fill=BOTH)
        self.perfs = PerfsFrame(self)
        self.perfs.pack(side=TOP, expand=1, fill=BOTH)
        self.file = FilesFrame(self)
        self.file.pack(side=TOP, expand=1, fill=BOTH)
        self.plot = PlotFrame(self)
        self.plot.pack(side=TOP, expand=1, fill=BOTH)

    def validate(self):
        valid = self.general.validate()
        valid = self.target.validate() and valid
        valid = self.perfs.validate() and valid
        valid = self.plot.validate() and valid
        return self.file.validate() and valid

    def lock(self):
        self.general.lock()
        self.target.lock()
        self.perfs.lock()
        self.file.lock()

    def unlock(self):
        self.general.unlock()
        self.target.unlock()
        self.perfs.unlock()
        self.file.unlock()
