import padasip as pa
import numpy as np


def least_mean_squares(inputSignal, targetSignal, mu, n):
    f = pa.filters.FilterLMS(n=n, mu=mu, w="random")
    y, e, w = f.run(targetSignal, inputSignal)
    return y, e


def normalized_least_mean_squares(inputSignal, targetSignal, mu, n):
    f = pa.filters.FilterNLMS(n=n, mu=mu, w="random")
    y, e, w = f.run(targetSignal, inputSignal)
    return y, e
