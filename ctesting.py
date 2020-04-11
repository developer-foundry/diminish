import numpy as np
import ctypes
import pathlib
import soundfile as sf
import argparse

def clean(inputString):
  if inputString is not None:
    inputString = inputString.strip()
  return inputString

if __name__ == "__main__":
  try:
    parser = argparse.ArgumentParser(description='Testing reading sound file and passing to C')
    parser.add_argument('-i', dest='inputFile', action='store', type=str,
                        help='input file')
    args = parser.parse_args()
    args.inputFile = clean(args.inputFile)

    # Load the shared library into ctypes
    libname = pathlib.Path().absolute() / "libcnumpy.so"
    c_lib = ctypes.CDLL(libname)
    print("Loaded shared library")

    inputSignal, sampleRate = sf.read(args.inputFile, dtype='float32')
    inputSignal = inputSignal[0:10]
    print(inputSignal.shape)
    c_float_p = ctypes.POINTER(ctypes.c_float)
    data = inputSignal.astype(np.float32)
    data_p = data.ctypes.data_as(c_float_p)
    c_lib.cnumpy(data_p, 10)
    for i in range(10):
      print("Python " + str(i) + " - " + str(inputSignal[i]))

  except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
