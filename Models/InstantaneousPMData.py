"""
The performance monitoring data at some instant
"""


class InstantaneousPMData:
    def __init__(self, power: float, ber: float, snr: float, dgd: float, qfactor: float, chromatic_dispersion: float, carrier_offset: float):
        """
        power: the instantaneous power levels
        ber: the instantaneous bit error rate
        snr: the instantaneous signal to noise ratio
        dgd: the instantaneous differential group delay
        qfactor: the instantaneous quality-factor
        chromatic_dispersion: the instantaneous chromatic dispersion
        carrier_offset: the instantaneous carrier offeset
        """
        self.power = power
        self.ber = ber
        self.snr = snr
        self.dgd = dgd
        self.qfactor = qfactor
        self.chromatic_dispersion = chromatic_dispersion
        self.carrier_offset = carrier_offset
