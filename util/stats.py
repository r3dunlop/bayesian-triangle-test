from scipy.special import comb
import numpy as np


def probability_of_x_differentiators(x, y, n):
    # x = number of true distinguishers
    # y = number of correct responses
    # n = total number of tasters
    numerator = comb(n - x, y - x) * np.power(1 / 3., y - x) * np.power(2 / 3., n - y)
    denominator = 0
    for u in range(y+1):
        denominator += comb(n - u, y - u) * np.power(1 / 3., y - u) * np.power(2 / 3., n - y)

    return numerator / denominator


def calculate_pvalue(y, n):
    y = np.arange(0, y)
    return 1 - np.sum(comb(n, y) * np.power(1. / 3, y) * np.power(2. / 3, n - y))