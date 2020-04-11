# ctypes_test.py
import ctypes
import pathlib

if __name__ == "__main__":
    # Load the shared library into ctypes
    libname = pathlib.Path().absolute() / "libcmult.so"
    c_lib = ctypes.CDLL(libname)
    print("Loaded shared library")
    x, y = 6, 2.3
    answer = c_lib.cmult(x, ctypes.c_float(y))
    print("In python returning result 13.8!")
