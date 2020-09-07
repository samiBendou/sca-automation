"""Python-agnostic SCA data parsing, logging and reporting module.

This module is designed as a class library providing *entity classes*
to represent the side channel data acquired from SoC.

It provides binary data parsing in order to read
acquisition data from a serial sources or a binary file and
retrieve it in the entity classes.

Examples
--------

>>> from lib import io
>>> from lib.data import Request, Parser
>>> request = Request(256)
>>> s = io.acquire_serial("/dev/ttyUSB1", request.command("sca"))
>>> parser = Parser(s)

>>> from lib import io
>>> from lib.data import Request, Parser
>>> request = Request(256)
>>> s = io.read_file("/path/to/file.bin")
>>> parser = Parser(s)

All the entity classes of the module provide CSV support
to allow processing acquisition data without parsing.
It also provides formatting data in a more human-readable format.

Examples
--------
>>> from lib import data
>>> meta = data.Meta("path/to/meta.csv")
>>> leak = data.Leak("path/to/leak.csv")
>>> # some processing on meta
>>> meta.write_csv("path/to/meta.csv",)

"""

import csv
import math
import os
from warnings import warn
from collections.abc import *


class Serializable:
    def write_csv(self, path: str, append: bool) -> None:
        pass


class Deserializable:
    def read_csv(self, path: str, count: int, start: int) -> None:
        pass


class Channel(MutableSequence, Reversible, Sized, Serializable, Deserializable):
    """Encryption channel data.

    This class is designed to represent AES 128 encryption data
    for each trace acquired.

    data are represented as 32-bit hexadecimal strings
    in order to accelerate IO operations on the encrypted block.

    Attributes
    ----------
    plains: list[str]
        Hexadecimal plain data of each trace.
    ciphers: list[str]
        Hexadecimal cipher data of each trace.
    keys: list[str]
        Hexadecimal key data of each trace.

    Raises
    ------
    ValueError
        If the three list attributes does not have the same length.

    """

    STR_MAX_LINES = 32

    def __init__(self, path=None, count=None, start=0):
        """Imports encryption data from CSV file.

        Parameters
        ----------
        path : str
            Path to the CSV to read.
        count : int, optional
            Count of rows to read.
        start: int, optional
            Index of first row to read.
        Returns
        -------
        Channel
            Imported encryption data.
        """
        self.plains = []
        self.ciphers = []
        self.keys = []

        if not path:
            return

        self.read_csv(path, count, start)

    def __getitem__(self, item):
        return self.plains[item], self.ciphers[item], self.keys[item]

    def __setitem__(self, item, value):
        plain, cipher, key = value
        self.plains[item] = plain
        self.ciphers[item] = cipher
        self.keys[item] = key

    def __delitem__(self, item):
        del self.plains[item]
        del self.ciphers[item]
        del self.keys[item]

    def __len__(self):
        return len(self.plains)

    def __iter__(self):
        return zip(self.plains, self.ciphers, self.keys)

    def __reversed__(self):
        return zip(reversed(self.plains), reversed(self.ciphers), reversed(self.keys))

    def __repr__(self):
        return f"{type(self).__name__}({self.plains!r}, {self.ciphers!r}, {self.keys!r})"

    def __str__(self):
        n = len(self.plains[0]) + 4
        ret = f"{'plains':<{n}s}{'ciphers':<{n}s}{'keys':<{n}s}"
        for d, (plain, cipher, key) in enumerate(self):
            if d == Channel.STR_MAX_LINES:
                return ret + f"\n{len(self) - d} more..."
            ret += f"\n{plain:<{n}s}{cipher:<{n}s}{key:<{n}s}"
        return ret

    def __iadd__(self, other):
        self.plains += other.plains
        self.ciphers += other.ciphers
        self.keys += other.keys
        return self

    def clear(self):
        """Clears all the attributes.

        """
        self.plains.clear()
        self.ciphers.clear()
        self.keys.clear()

    def append(self, item):
        plain, cipher, key = item
        self.plains.append(plain)
        self.ciphers.append(cipher)
        self.keys.append(key)

    def pop(self, **kwargs):
        self.plains.pop()
        self.ciphers.pop()
        self.keys.pop()

    def insert(self, index: int, item):
        plain, cipher, key = item
        self.plains.insert(index, plain)
        self.ciphers.insert(index, cipher)
        self.keys.insert(index, key)

    def write_csv(self, path, append=False):
        """Exports encryption data to a CSV file.

        Parameters
        ----------
        path : str
            Path to the CSV file to write.
        append : bool, optional
            True to append the data to an existing file.
        """
        try:
            file = open(path, "x+" if append else "w+", newline="")
            append = False
        except FileExistsError:
            file = open(path, "a+")
        writer = csv.DictWriter(file, [Keywords.PLAIN, Keywords.CIPHER, Keywords.KEY], delimiter=";")
        if not append:
            writer.writeheader()
        for plain, cipher, key in self:
            writer.writerow({Keywords.PLAIN: plain,
                             Keywords.CIPHER: cipher,
                             Keywords.KEY: key})
        file.close()

    def read_csv(self, path=None, count=None, start=0):
        count = count or math.inf
        with open(path, "r", newline="") as file:
            reader = csv.DictReader(file, delimiter=";")
            for d, row in enumerate(reader):
                if d < start:
                    continue
                if d >= count + start:
                    break
                self.plains.append(row[Keywords.PLAIN])
                self.ciphers.append(row[Keywords.CIPHER])
                self.keys.append(row[Keywords.KEY])

        if len(self.plains) != len(self.ciphers) or len(self.plains) != len(self.keys):
            raise ValueError("Inconsistent plains, cipher and keys length")


class Leak(MutableSequence, Reversible, Sized, Serializable, Deserializable):
    """Side-channel leakage data.

    This class represents the power consumption traces
    acquired during encryption in order to process these.

    Attributes
    ----------
    samples: list[int]
        Count of samples for each traces.
    traces: list[list[int]]
        Power consumption leakage signal for each acquisition.

    """

    STR_MAX_LINES = 32

    def __init__(self, path=None, count=None, start=0):
        """Imports leakage data from CSV.

        Parameters
        ----------
        path : str
            Path to the CSV to read.
        count : int, optional
            Count of rows to read.
        start: int, optional
            Index of first row to read.
        Returns
        -------
        Leak
            Imported leak data.
        """

        self.traces = []
        self.samples = []
        if not path:
            return
        self.read_csv(path, count, start)

    def __getitem__(self, item):
        return self.traces[item]

    def __setitem__(self, item, value):
        self.traces[item] = value
        self.samples[item] = len(value)

    def __delitem__(self, item):
        del self.traces[item]
        del self.samples[item]

    def __len__(self):
        return len(self.traces)

    def __iter__(self):
        return iter(self.traces)

    def __reversed__(self):
        return iter(reversed(self.traces))

    def __repr__(self):
        return f"{type(self).__name__}({self.traces!r})"

    def __str__(self):
        ret = f"{'no.':<16s}traces"
        for d, trace in enumerate(self):
            if d == Leak.STR_MAX_LINES:
                return ret + f"\n{len(self) - d} more..."
            ret += f"\n{d:<16d}"
            for t in trace:
                ret += f"{t:<4d}"
        return ret

    def __iadd__(self, other):
        self.traces += other.traces
        self.samples += other.samples
        return self

    def clear(self):
        self.traces.clear()
        self.samples.clear()

    def append(self, item):
        self.traces.append(item)
        self.samples.append(len(item))

    def pop(self, **kwargs):
        self.traces.pop()
        self.samples.pop()

    def insert(self, index, item):
        self.traces.insert(index, item)
        self.samples.insert(index, len(item))

    def write_csv(self, path, append=False):
        """Exports leakage data to CSV.

        Parameters
        ----------
        path : str
            Path to the CSV file to write.
        append : bool, optional
            True to append the data to an existing file.
        """
        with open(path, "a+" if append else "w+", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(self.traces)

    def read_csv(self, path, count=None, start=0):
        count = count or math.inf
        with open(path, "r", newline="") as file:
            reader = csv.reader(file, delimiter=";")
            for d, row in enumerate(reader):
                if d < start:
                    continue
                if d >= count + start:
                    break
                self.traces.append(list(map(lambda x: int(x), row)))
                self.samples.append(len(self.traces[-1]))


class Meta(Serializable, Deserializable):
    """Meta-data of acquisition.

   This class is designed to represent additional infos
   about the current side-channel acquisition run.

    Attributes
    ----------
    mode : str
        Encryption mode.
    direction : str
        Encryption direction, either encrypt or decrypt.
    target : int
        Sensors calibration target value.
    sensors : int
        Count of sensors.
    iterations : int
        Requested count of traces.
    offset : int
        If the traces are ASCII encoded, code offset
    """

    def __init__(self, path=None, count=None, start=0):
        """Imports meta-data from CSV file.

        If the file is empty returns an empty meta data object.

        Parameters
        ----------
        path : str
            Path to the CSV to read.

        Returns
        -------
        Meta
            Imported meta-data.
        """

        self.mode = None
        self.direction = None
        self.target = 0
        self.sensors = 0
        self.iterations = 0
        self.offset = 0

        if not path:
            return

        self.read_csv(path, count, start)

    def __repr__(self):
        return f"{type(self).__name__}(" \
               f"{self.mode!r}, " \
               f"{self.direction!r}, " \
               f"{self.target!r}, " \
               f"{self.sensors!r}, " \
               f"{self.iterations!r}, " \
               f"{self.offset!r})"

    def __str__(self):
        dl = str(Keywords.DELIMITER, 'ascii')
        return f"{Keywords.MODE}{dl} {self.mode}\n" \
               f"{Keywords.DIRECTION}{dl} {self.direction}\n" \
               f"{Keywords.TARGET}{dl} {self.target}\n" \
               f"{Keywords.SENSORS}{dl} {self.sensors}\n" \
               f"{Keywords.ITERATIONS}{dl} {self.iterations}\n" \
               f"{Keywords.OFFSET}{dl} {self.offset}"

    def clear(self):
        """Resets meta-data.

        """
        self.mode = None
        self.direction = None
        self.target = 0
        self.sensors = 0
        self.iterations = 0
        self.offset = 0

    def write_csv(self, path, append=False):
        """Exports meta-data to a CSV file.

        Parameters
        ----------
        path : str
            Path to the CSV file to write.
        append : bool, optional
        """
        try:
            file = open(path, "x+" if append else "w+", newline="")
        except FileExistsError:
            meta = Meta(path)
            self.iterations += meta.iterations
            file = open(path, "w+", newline="")

        fieldnames = [Keywords.MODE,
                      Keywords.DIRECTION,
                      Keywords.TARGET,
                      Keywords.SENSORS,
                      Keywords.ITERATIONS,
                      Keywords.OFFSET]
        writer = csv.DictWriter(file, fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerow({Keywords.MODE: self.mode,
                         Keywords.DIRECTION: self.direction,
                         Keywords.TARGET: self.target,
                         Keywords.SENSORS: self.sensors,
                         Keywords.ITERATIONS: self.iterations,
                         Keywords.OFFSET: self.offset})
        file.close()

    def read_csv(self, path, count=None, start=0):
        with open(path, "r", newline="") as file:
            reader = csv.DictReader(file, delimiter=";")
            try:
                row = next(reader)
            except StopIteration:
                return
            self.mode = row[Keywords.MODE]
            self.direction = row[Keywords.DIRECTION]
            self.target = int(row[Keywords.TARGET])
            self.sensors = int(row[Keywords.SENSORS])
            self.iterations = int(row[Keywords.ITERATIONS])
            self.offset = int(row[Keywords.OFFSET])

            count = count or math.inf
            for d, row in enumerate(reader):
                if d < start:
                    continue
                if d >= count + start:
                    break
                self.iterations += int(row[Keywords.ITERATIONS])


class Request:
    """Data processing request.

    This class provides a simple abstraction to wrap
    file naming arguments during acquisition, import or export.

    The these arguments combined together form a *data request*
    specifying all the characteristics of the target data-set.

    Attributes
    ----------
    name : str
        Serial port id or file prefix according to the source mode.
    iterations : int
        Requested count of traces.
    mode : str
        Encryption mode.
    direction : str
        Encrypt direction.
    source : str
        Source mode.
    verbose : True
        True to perform verbose acquisition.
    chunks : int, optional
        Count of chunks to acquire or None if not performing chunk acquisition
    """

    ACQ_CMD_NAME = "sca"

    class Modes:
        HARDWARE = "hw"
        SOFTWARE = "sw"

    class Directions:
        ENCRYPT = "enc"
        DECRYPT = "dec"

    class Sources:
        FILE = "file"
        SERIAL = "serial"

    def __init__(self, args=None):
        """Initializes a request with a previously parsed command.

        Parameters
        ----------
        args
            Parsed arguments.

        """
        self.name = None
        self.iterations = args.iterations
        self.source = Request.Sources.FILE
        self.mode = Request.Modes.HARDWARE
        self.direction = Request.Directions.ENCRYPT
        self.verbose = False
        self.chunks = None

        if hasattr(args, "name"):
            self.name = args.name
        if hasattr(args, "source"):
            self.source = args.source
        if hasattr(args, "mode"):
            self.mode = args.mode
        if hasattr(args, "direction"):
            self.direction = args.direction
        if hasattr(args, "verbose"):
            self.verbose = args.verbose
        if hasattr(args, "chunks"):
            self.chunks = args.chunks

    def __repr__(self):
        return f"{type(self).__name__}" \
               f"({self.name}, " \
               f"{self.iterations}, " \
               f"{self.source}, " \
               f"{self.mode}, " \
               f"{self.direction}, " \
               f"{self.verbose}, " \
               f"{self.chunks})"

    def __str__(self):
        return f"{'name':<16}{self.name}\n" \
               f"{'iterations':<16}{self.iterations}\n" \
               f"{'source':<16}{self.source}\n" \
               f"{'mode':<16}{self.mode}\n" \
               f"{'direction':<16}{self.direction}\n" \
               f"{'verbose':<16}{self.verbose}\n" \
               f"{'chunks':<16}{self.chunks}"

    def filename(self, prefix=None, suffix=""):
        """Creates a filename based on the request.

        This method allows to consistently name the files
        according to request's characteristics.

        Parameters
        ----------
        prefix : str
            Prefix of the filename.
        suffix : str, optional
            Suffix of the filename.

        Returns
        -------
        str :
            The complete filename.

        """
        iterations = self.iterations * (self.chunks or 1)
        return f"{prefix or self.name.split(os.sep)[-1]}_{self.mode}_{self.direction}_{iterations}{suffix}"

    def command(self, name):
        return "{}{}{}{}{}".format(name,
                                   " -t %d" % self.iterations,
                                   " -v" if self.verbose else "",
                                   " -h" if self.mode == Request.Modes.HARDWARE else "",
                                   " -i" if self.direction == Request.Directions.DECRYPT else "")


class Keywords:
    """Iterates over the binary log keywords.

    This iterator allows to represent the keywords and
    the order in which they appear in the binary log consistently.

    This feature is useful when parsing log lines in order
    to avoid inserting a sequence that came in the wrong order.

    At each iteration the next expected keyword is returned.

    ``meta`` attribute allows to avoid expect again meta keywords
    when an error occurs and the iterator must be reset.

    Attributes
    ----------
    idx: int
        Current keyword index.
    meta: bool
        True if the meta-data keyword have already been browsed.
    inv: bool
        True if the keywords follow the inverse encryption sequence.
    metawords: str
        Keywords displayed once at the beginning of acquisition.
    datawords: str
        Keywords displayed recurrently during each trace acquisition.
    value: str
        Value of the current keyword.

    """

    MODE = "mode"
    DIRECTION = "direction"
    SENSORS = "sensors"
    TARGET = "target"
    KEY = "keys"
    PLAIN = "plains"
    CIPHER = "ciphers"
    SAMPLES = "samples"
    CODE = "code"
    WEIGHTS = "weights"
    OFFSET = "offset"
    ITERATIONS = "iterations"

    DELIMITER = b":"
    START_TRACE_TAG = b"\xfe\xfe\xfe\xfe"
    END_ACQ_TAG = b"\xff\xff\xff\xff"

    def __init__(self, meta=False, inv=False, verbose=False):
        """Initializes a new keyword iterator.

        Parameters
        ----------
        meta : bool
            If true, meta-data keywords will be ignored.
        inv: bool
            True if the keywords follow the inverse encryption sequence.
        """
        self.idx = 0
        self.meta = meta
        self.value = ""
        self.__build_metawords()
        self.__build_datawords(inv, verbose)
        self.reset()

    def __iter__(self):
        return self

    def __next__(self):
        current = self.value
        if self.meta:
            self.idx = (self.idx + 1) % len(self.datawords)
            self.value = self.datawords[self.idx]
            return current

        if self.idx < len(self.metawords):
            self.idx += 1

        if self.idx == len(self.metawords):
            self.reset(meta=True)
            return current

        self.value = self.metawords[self.idx]
        return current

    def reset(self, meta=None):
        self.idx = 0
        self.meta = meta or self.meta
        self.value = self.datawords[0] if self.meta else self.metawords[0]

    def __build_metawords(self):
        self.metawords = [Keywords.SENSORS, Keywords.TARGET, Keywords.MODE, Keywords.DIRECTION, Keywords.KEY]

    def __build_datawords(self, inv, verbose):
        self.datawords = [Keywords.CIPHER, Keywords.PLAIN] if inv else [Keywords.PLAIN, Keywords.CIPHER]
        self.datawords += [Keywords.SAMPLES, Keywords.WEIGHTS] if verbose else [Keywords.SAMPLES, Keywords.CODE]


class Parser:
    """Binary data parser.

    This class is designed to parse binary acquisition data
    and store parsed data in the entity classes in order
    to later import and export it.

    Attributes
    ----------
    leak : Leak
        Leakage data.
    channel : Channel
        Encryption data.
    meta : Meta
        Meta-data.

    See Also
    --------
    Keywords : iterator representing the keyword sequence

    """

    def __init__(self, s=b"", direction=Request.Directions.ENCRYPT):
        """Initializes an object with binary data.

        Parameters
        ----------
        s : bytes
            Binary data.
        direction : str
            Encryption direction.
        Returns
        -------
        Parser
            Parser initialized with data.

        """
        self.leak = Leak()
        self.channel = Channel()
        self.meta = Meta()
        self.parse(s, direction)

    def pop(self):
        """Pops acquired value until data lengths matches.

        This method allows to guarantee that the data contained
        in the parser will always have the same length which is
        the number of traces parsed.

        Returns
        -------
        Parser
            Reference to self.
        """
        lens = list(map(len, [
            self.channel.keys, self.channel.plains, self.channel.ciphers, self.leak.samples, self.leak.traces
        ]))
        n_min = min(lens)
        n_max = max(lens)

        if n_max == n_min:
            self.leak.pop()
            self.channel.pop()
            self.meta.iterations -= 1
            return

        while len(self.leak.samples) != n_min:
            self.leak.samples.pop()
        while len(self.leak.traces) != n_min:
            self.leak.traces.pop()
        while len(self.channel.keys) != n_min:
            self.channel.keys.pop()
        while len(self.channel.plains) != n_min:
            self.channel.plains.pop()
        while len(self.channel.ciphers) != n_min:
            self.channel.ciphers.pop()

        return self

    def clear(self):
        """Clears all the parser data.

        """
        self.leak.clear()
        self.meta.clear()
        self.channel.clear()

    def parse(self, s, direction=Request.Directions.ENCRYPT):
        """Parses the given bytes to retrieve acquisition data.

        If inv`` is not specified the parser will infer the
        encryption direction from ``s``.

        Parameters
        ----------
        s : bytes
            Binary data.
        direction : str
            Encryption direction.

        Returns
        -------
        Parser
            Reference to self.
        """
        keywords = Keywords(inv=direction == Request.Directions.DECRYPT)
        expected = next(keywords)
        valid = True
        lines = s.split(b"\r\n")
        for idx, line in enumerate(lines):
            if valid is False:
                valid = line == Keywords.START_TRACE_TAG
                continue
            try:
                if self.__parse_line(line, expected):
                    expected = next(keywords)
            except (ValueError, UnicodeDecodeError, RuntimeError) as e:
                args = (e, len(self.leak.traces), idx, line)
                warn("parsing error\nerror: {}\niteration: {:d}\nline {:d}: {}".format(*args))
                keywords.reset(keywords.meta)
                expected = next(keywords)
                valid = False
                self.pop()

        if len(self.channel.keys) == 1:
            self.channel.keys = [self.channel.keys[0]] * len(self.channel)
        self.meta.iterations += len(self.channel)
        return self

    def __parse_line(self, line, expected):
        if line in (Keywords.END_ACQ_TAG, Keywords.START_TRACE_TAG):
            return False
        split = line.strip().split(Keywords.DELIMITER)
        try:
            keyword = str(split[0], "ascii").strip()
            data = split[1].strip()
        except IndexError:
            return False

        if keyword != expected:
            raise RuntimeError("expected %s keyword not %s" % (expected, keyword))

        if keyword in (Keywords.MODE, Keywords.DIRECTION):
            setattr(self.meta, keyword, str(data, "ascii"))
        elif keyword in (Keywords.SENSORS, Keywords.TARGET):
            setattr(self.meta, keyword, int(data))
        elif keyword in (Keywords.KEY, Keywords.PLAIN, Keywords.CIPHER):
            getattr(self.channel, keyword).append(f"{int(data.replace(b' ', b''), 16):x}")
        elif keyword == Keywords.SAMPLES:
            self.leak.samples.append(int(data))
        elif keyword == Keywords.CODE:
            self.leak.traces.append(list(map(lambda c: int(c) + self.meta.offset, line[(len(Keywords.CODE) + 2):])))
        elif keyword == Keywords.WEIGHTS:
            self.leak.traces.append(list(map(int, data.split(b","))))
        else:
            return False

        if keyword == Keywords.TARGET:
            self.meta.offset = self.meta.sensors * self.meta.target - ord("P")

        if keyword in (Keywords.CODE, Keywords.WEIGHTS):
            n = self.leak.samples[-1]
            m = len(self.leak.traces[-1])
            if m != n:
                raise RuntimeError("trace lengths mismatch %d != %d" % (m, n))

        return True
