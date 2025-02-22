"""
The device module:
Contains the definition of class Device and prebuilt devices for physical measurement.
"""
import uncertainties

from _utils import _is_numeric, _is_iterable, tp_factor
import logging, math

import numpy
from numpy import array

from constant import confidence

class Device(object):
    def __init__(self, tolerance, scaling_factor=1.):
        self.tolerance = tolerance
        self.scaling_factor = scaling_factor

    def measure(self, data: any, processor = None, apply_scaling=False):
        if processor is not None:
            data = processor(data)
        # The value to return:
        value = None
        # The two types of deviations:
        deviation_a = 0
        deviation_b = self.tolerance * confidence * (self.scaling_factor if apply_scaling else 1)
        if _is_numeric(data):
            value = data
            if apply_scaling:
                value *= self.scaling_factor
        elif _is_iterable(data):
            # Convert into a numpy array:
            try:
                data = array(data)
            except:
                raise TypeError('data cannot be converted to a numpy array')
            if apply_scaling:
                for i in range(len(data)):
                    data[i] *= self.scaling_factor
            # Generate the A-type deviation:
            std_dev = numpy.std(data, ddof=1)
            logging.info(f"array: σ = {std_dev}")
            tp = tp_factor(data.size, confidence=confidence)
            deviation_a = std_dev * tp / math.sqrt(len(data))
            value = data.mean()
        else:
            raise TypeError('the data is neither numeric nor iterable')

        logging.info(f"array: ΔA = {deviation_a}")
        logging.info(f"array: ΔB = {deviation_b}")

        return uncertainties.ufloat(value, math.sqrt(deviation_a ** 2 + deviation_b ** 2))

# Commonly used devices are defined afterward
# The scaling factors correspond to that of SI
# - length
ruler = Device(0.1, 1E-3)
meter_ruler = Device(0.005, 1)
vernier = Device(0.02, 1E-3)
microscrew = Device(0.004, 1E-3)
# - time
timer = Device(0.01, 1)
# - mass
balance = Device(0.001, 1E-3)
# - temperature
thermostat = Device(0.5, 1)
# - compound
density_meter = Device(0.0001, 1E3)