import numpy as np
from abc import ABC

class Channel(ABC):
    def __init__(self, param):
        self.param = param

    def send(self, x):
        pass

    def llrs(self, y):
        pass


class BSC(Channel):
    name = "bsc"
   
    def __init__(self, param):
        self.param = param

    def send(self, x):
        return (x + (np.random.random(x.shape) < self.param)) % 2

    def llrs(self, y):
        return (1-2*y)*(np.log(1 - self.param) - np.log(self.param))


def channel_factory(channel_name):
    channels_dict = {"bsc": BSC}
    return channels_dict.get(channel_name)
