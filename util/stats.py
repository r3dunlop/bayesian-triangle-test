from scipy.special import comb
import numpy as np


def probability_of_x_discriminators(x, y, n):
    # x = number of true distinguishers
    # y = number of correct responses
    # n = total number of tasters
    numerator = comb(n - x, y - x) * np.power(1 / 3., y - x) * np.power(2 / 3., n - y)
    u = np.arange(0, y + 1 )
    denominator = np.sum(comb(n - u, y - u) * np.power(1 / 3., y - u) * np.power(2 / 3., n - y))

    return numerator / denominator

def probability_of_more_than_x_discriminators(x, y, n):
    x_list = list(x)
    rtn_list = []
    for i in x_list:
        r = np.arange(i+1, y+1)
        rtn_list.append(np.sum(probability_of_x_discriminators(r, y, n)))

    return rtn_list

def calculate_pvalue(y, n):
    y = np.arange(0, y)
    return 1 - np.sum(comb(n, y) * np.power(1. / 3, y) * np.power(2. / 3, n - y))