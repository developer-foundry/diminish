import numpy as np
import ctypes
import pathlib
import pprint


class Signal(ctypes.Structure):
    _fields_ = [("channel_one", ctypes.POINTER(ctypes.c_double)),
                ("channel_two", ctypes.POINTER(ctypes.c_double)),
                ("channel_one_start", ctypes.POINTER(ctypes.c_double)),
                ("channel_two_start", ctypes.POINTER(ctypes.c_double)),
                ("length", ctypes.c_int)
                ]


def crls(inputSignal, targetSignal, mu, n):
    length = inputSignal.shape[0]
    libname = pathlib.Path().absolute() / "filtering.so"
    c_double_p = ctypes.POINTER(ctypes.c_double)
    c_lib = ctypes.CDLL(libname)
    c_lib.rls.argtypes = [c_double_p, c_double_p, ctypes.c_double,
                          ctypes.c_int, c_double_p, c_double_p, ctypes.c_int]

    inputSignal = inputSignal[0:length]
    inputSignalData = inputSignal.astype(np.float64)
    inputSignal_p = inputSignalData.ctypes.data_as(c_double_p)

    targetSignal = targetSignal[0:length]
    targetSignalData = targetSignal.astype(np.float64)
    targetSignal_p = targetSignalData.ctypes.data_as(c_double_p)

    y = (ctypes.c_double * length)()
    e = (ctypes.c_double * (length))()

    c_lib.rls(targetSignal_p, inputSignal_p, mu, n, y, e, length)

    return y, e
