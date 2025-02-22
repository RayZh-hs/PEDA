from peda.device import ruler, microscrew
from math import pi
import logging

logging.basicConfig(level=logging.DEBUG)

print(microscrew.measure(1.954, apply_scaling=True))