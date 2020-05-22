import numpy as np
import ctypes
import pathlib
import pprint


def crls(inputSignal, targetSignal, mu, n):
    """RLS signal processing algorithm. The python code will call a C implementation of RLS

    Parameters
    ----------
    inputSignal : np.array
        Input matrix (2-dimensional array). Rows are samples. Columns are input arrays.
    targetSignal : np.array
        Target matrix (2-dimensional array). Rows are samples. Columns are input arrays.
    mu : float
        It is introduced to give exponentially less weight to older error samples. It is usually chosen between 0.98 and 1.
    n : int
        The number of samples in the dataset.

    Returns
    -------
    y : np.array
        An array of data representing the output signal
    e : np.array
        Ar array of data representing the error singal

    Raises
    ------
    None
    """
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
