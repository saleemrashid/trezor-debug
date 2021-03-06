#!/usr/bin/env python3
import code
import readline
import rlcompleter
import struct
import sys

from trezorlib.device import TrezorDevice

import trezorlib.messages as proto

try:
    transport, = (device.find_debug() for device in TrezorDevice.enumerate())
except ValueError:
    sys.exit("Exactly one TREZOR must be connected, with debug link enabled.")

transport.session_begin()


class HexInteger(int):
    def __repr__(self):
        return hex(self)


class MemoryMappedInteger(object):
    def __init__(self, fmt, address):
        self.struct = struct.Struct("<" + fmt)
        self.address = address

    def read(self):
        transport.write(proto.DebugLinkMemoryRead(
            address=self.address,
            length=self.struct.size,
        ))
        msg = transport.read()

        data, = self.struct.unpack(msg.memory)
        return HexInteger(data)

    def write(self, data):
        memory = self.struct.pack(data)
        transport.write(proto.DebugLinkMemoryWrite(
            address=self.address,
            memory=memory,
            flash=False
        ))


class MMIO8(MemoryMappedInteger):
    def __init__(self, address):
        super().__init__("B", address)


class MMIO16(MemoryMappedInteger):
    def __init__(self, address):
        super().__init__("H", address)


class MMIO32(MemoryMappedInteger):
    def __init__(self, address):
        super().__init__("I", address)


class MMIO64(MemoryMappedInteger):
    def __init__(self, address):
        super().__init__("Q", address)


class MemoryMappedScope(dict):
    def __init__(self):
        self["MMIO8"] = MMIO8
        self["MMIO16"] = MMIO16
        self["MMIO32"] = MMIO32
        self["MMIO64"] = MMIO64

        self["execfile"] = self.execfile

    def __getitem__(self, key):
        value = super().__getitem__(key)

        if isinstance(value, MemoryMappedInteger):
            return value.read()

        if isinstance(value, int):
            return HexInteger(value)

        return value

    def __setitem__(self, key, value):
        if key in self:
            existing = super().__getitem__(key)

            if isinstance(existing, MemoryMappedInteger):
                existing.write(value)
                return

        super().__setitem__(key, value)

    def execfile(self, filename):
        exec(compile(open(filename).read(), filename, "exec"), self)

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)


scope = MemoryMappedScope()
scope.execfile("generated.py")

readline.set_completer(rlcompleter.Completer(scope).complete)
readline.parse_and_bind("tab: complete")
code.interact(local=scope)
