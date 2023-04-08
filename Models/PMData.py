"""
Performance Monitoring Data. Contains both instantaneous data and summary statistics of the data within the last 15 minutes of the instant
"""
from models.InstantaneousPMData import InstantaneousPMData
from models.FifteenMinuteBinnedPMData import FifteenMinuteBinnedPMData


class PMData:
    def __init__(self, instantaneous: InstantaneousPMData, fifteen_minute_bin: FifteenMinuteBinnedPMData) -> None:
        """
        instantaneous: the instantaneous performance monitoring data
        fifteen_minute_bin: summary statistics of the last fifteen-minute bin
        """
        self.instantaneous = instantaneous
        self.fifteen_minute_bin = fifteen_minute_bin
