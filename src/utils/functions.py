import numpy as np


class Functions:
    @staticmethod
    def linear(x: list, k, b):
        return [k * i + b for i in x]


    @staticmethod
    def exponential(x: list, k, b):
        return [np.exp(k * i + b) for i in x]


    @staticmethod
    def power(x: list, n, c):
        return [c * (i**n) for i in x]