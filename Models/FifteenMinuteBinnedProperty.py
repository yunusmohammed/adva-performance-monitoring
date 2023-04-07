"""
Summary statistics of a fifteen-minute binned performance monitoring datapoint
"""


class FifteenMinuteBinnedProperty:
    def __init__(self, low: float, median: float, high: float) -> None:
        """
        low: the lowest recorded value within the fifteen minute bin
        median: the median recorded value within the fifteen minute bin
        high: the highest recorded value within the fifteen minute bin
        """
        self.low = low
        self.median = median
        self.high = high
