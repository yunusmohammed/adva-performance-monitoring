"""
The performance monitoring data of a 15-minute bin
"""
from models.FifteenMinuteBinnedProperty import FifteenMinuteBinnedProperty


class FifteenMinuteBinnedPMData:
    def __init__(self, power: FifteenMinuteBinnedProperty, ber: FifteenMinuteBinnedProperty, snr: FifteenMinuteBinnedProperty, dgd: FifteenMinuteBinnedProperty, qfactor: FifteenMinuteBinnedProperty, chromatic_dispersion: FifteenMinuteBinnedProperty, carrier_offset: FifteenMinuteBinnedProperty) -> None:
        """
        power: summary of the power levels of a 15-minute bin
        ber: summary of the bit error rate of a 15-minute bin
        snr: summary of the signal to noise ratio of a 15-minute bin
        dgd: summary of the differential group delay of a 15-minute bin
        qfactor: summary of the quality factor of a 15-minute bin
        chromatic_dispersion: summary of the chromatic dispersion of a 15-minute bin
        carrier_offset: summary of the carrier offset of a 15-minute bin
        """
        self.power = power
        self.ber = ber
        self.snr = snr
        self.dgd = dgd
        self.qfactor = qfactor
        self.chromatic_dispersion = chromatic_dispersion
        self.carrier_offset = carrier_offset
