import padasip as pa


def least_mean_squares(inputSignal, targetSignal, mu):
    f = pa.filters.FilterLMS(n=inputSignal.shape[0], mu=mu, w="random")
    y, e, w = f.run(targetSignal, inputSignal)
    return y, e


def normalized_least_mean_squares(inputSignal, targetSignal, mu):
    f = pa.filters.FilterNLMS(n=inputSignal.shape[0], mu=mu, w="random")
    y, e, w = f.run(targetSignal, inputSignal)
    return y, e
