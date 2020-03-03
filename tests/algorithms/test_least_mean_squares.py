import pytest
from soundwave.algorithms.least_mean_squares import least_mean_squares

def test_least_mean_squares():
  least_mean_squares(0)
  assert True