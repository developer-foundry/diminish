import padasip as pa
import numpy as np
import ctypes
import pathlib

class Signal(ctypes.Structure):
    ctypes.c_wchar_p
    _fields_=[("channel_one",ctypes.POINTER(ctypes.c_float)),
              ("channel_two",ctypes.POINTER(ctypes.c_float)),
              ("channel_one_start",ctypes.POINTER(ctypes.c_float)),
              ("channel_two_start",ctypes.POINTER(ctypes.c_float)),
              ("length",ctypes.c_int)
        ]

def clms(inputSignal, targetSignal, mu, n):
    sampleSize = 10 # just here for debugging right now
    libname = pathlib.Path().absolute() / "libclms.so"
    c_lib = ctypes.CDLL(libname)
    c_lib.lms.restype = ctypes.POINTER(Signal)

    c_float_p = ctypes.POINTER(ctypes.c_float)
    data = inputSignal.astype(np.float32)
    data_p = data.ctypes.data_as(c_float_p)
    retSignal = c_lib.lms(data_p, sampleSize)

    for i in range(sampleSize):
      print("LMS Output %d - [%1.6f, %1.6f]" % (i,
                                                retSignal.contents.channel_one[i],
                                                retSignal.contents.channel_two[i]))
    return [0], [0]

def lms(inputSignal, targetSignal, mu, n):
    f = pa.filters.FilterLMS(n=n, mu=mu, w="random")
    y, e, w = f.run(targetSignal, inputSignal)
    return y, e


def nlms(inputSignal, targetSignal, mu, n):
    f = pa.filters.FilterNLMS(n=n, mu=mu, w="random")
    y, e, w = f.run(targetSignal, inputSignal)
    return y, e


def nsslms(inputSignal, targetSignal, mu, n):
    f = pa.filters.FilterNSSLMS(n=n, mu=mu, w="random")
    y, e, w = f.run(targetSignal, inputSignal)
    return y, e

def rls(inputSignal, targetSignal, mu, n):
    f = pa.filters.FilterRLS(n=n, mu=mu, w="random")
    y, e, w = f.run(targetSignal, inputSignal)
    return y, e
