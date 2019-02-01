# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name,missing-docstring,missing-param-doc

"""
Container for functional pulse
"""

from qiskit.pulse.commands.pulse_command import PulseCommand


class SamplePulse(PulseCommand):
    """Container for functional pulse."""

    def __init__(self, sample):
        """create new sample pulse command

        Parameters:
            name (str): name of the pulse. this is a unique string identifier used to refer to the
            pulse in the command sequence for the experiment.

            sample (list): list of complex values, which define the amplitude points for
            the pulse envelope. The time between the amplitude points is specified by
            the device time unit dt. these amplitudes have an absolute value less than
            or equal to 1.
        """

        super(SamplePulse, self).__init__(len(sample))

        self.sample = sample
