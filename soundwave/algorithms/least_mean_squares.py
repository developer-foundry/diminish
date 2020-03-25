import padasip as pa
import numpy as np


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
