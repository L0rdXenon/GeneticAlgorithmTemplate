import numpy as np
import matplotlib.pyplot as plt

def sine(x, period=100, offset=0, max=1):
    x = x+offset
    return (np.sin(2*x*np.pi/period)/2 + 0.5) * max

def sawtooth(x, period=100, offset = 0, max=1):
    x = x+offset
    return ((x%period)/period) * max

def descendingSawtooth(x, period=100, offset = 0, max=1):
    x = x+offset
    x = -x
    return ((x%period)/period) * max

def exponentialsawtooth(x, period=100, offset = 0, exponent=2, max=1):
    x = x+offset
    return (((x%period)/period) ** exponent) * max

def exponentialsine(x, period=100, offset = 0, exponent=2, max=1):
    x = x+offset
    return ((np.sin(2*x*np.pi/period)/2 + 0.5) ** exponent) * max

def exponentialDecay(x, alpha=0.99, max=0.05, offset=0):
    x = x+offset
    return (alpha ** x) * max

def repeatedExponentialDecay(x, period=100, offset = 0, alpha=0.98, beta=0.9, max=0.05):
    x = x+offset
    res = np.zeros(shape=x.shape)
    for i in range(0, len(x), period):
        res[i:] = (beta ** (i/period)) * (alpha ** x[:len(x) - i]) * max
        #print((beta ** i))
    return res

def linearDecrease(x, maximum = 1, offset=0):
    x = x+offset
    return (max(x) - x) * maximum/max(x)