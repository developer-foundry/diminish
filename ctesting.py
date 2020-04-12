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

    sampleSize = 10
    inputSignal, sampleRate = sf.read(args.inputFile, dtype='float32')
    inputSignal = inputSignal[0:sampleSize]
    c_float_p = ctypes.POINTER(ctypes.c_float)
    data = inputSignal.astype(np.float32)
    data_p = data.ctypes.data_as(c_float_p)
    c_lib.cnumpy(data_p, sampleSize)
    for i in range(sampleSize):
      print("Python Sample %d - [%1.6f, %1.6f]" % (i, inputSignal[i][0], inputSignal[i][1]))

  except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
