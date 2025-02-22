from scipy.stats import t
from collections.abc import Iterable

def _is_numeric(thing: any):
    return isinstance(thing, (int, float))

def _is_iterable(thing: any):
    return isinstance(thing, Iterable)

def tp_factor(n, confidence):
    """Calculate the tp correction factor for a given sample size n and confidence level."""
    df = n - 1  # Degrees of freedom
    alpha = 1 - confidence  # Significance level
    tp = t.ppf(1 - alpha / 2, df)  # Two-tailed t-critical value
    return tp