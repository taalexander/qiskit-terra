# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name,missing-docstring,missing-param-doc

"""
Functional Pulse
"""

import warnings
from inspect import signature

import numpy as np

from qiskit.exceptions import QiskitError
from qiskit.pulse.commands.sample_pulse import SamplePulse


class FunctionalPulse:
    """Functional pulse decorator"""

    def __init__(self, pulse):
        """Decorate pulse envelope function.

        Args:
            pulse (callable): a function describing pulse envelope
        Raises:
            QiskitError: when incorrect envelope function is specified
        """

        if callable(pulse):
            sig = signature(pulse)
            if 'duration' in sig.parameters:
                self.pulse = pulse
            else:
                raise QiskitError('Pulse function requires "duration" argument.')
        else:
            raise QiskitError('Pulse function is not callable.')

    def __call__(self, duration, **kwargs):
        """Return Functional Pulse with methods
        """
        return _FunctionalPulse(self.pulse, duration=duration, **kwargs)


class _FunctionalPulse:
    """Sample Pulse generation from functional pulse."""

    def __init__(self, pulse, duration, **kwargs):
        """ Generate new functional pulse

        Args:
            pulse (callable): a function describing pulse envelope
            duration (float): pulse duration
        """
        self.pulse = pulse
        self.duration = duration
        self._params = kwargs

    @property
    def params(self):
        """Get parameters for describing pulse envelope

        Returns:
            dict: pulse parameters
        """
        return self._params

    @params.setter
    def params(self, params_new):
        """Set parameters for describing pulse envelope

        Args:
            params_new (dict): dictionary of parameters
        Raises:
            QiskitError: when pulse parameter is not in the correct format.
        """
        if isinstance(params_new, dict):
            for key, val in self._params.items():
                self._params[key] = params_new.get(key, val)
        else:
            raise QiskitError('Pulse parameter should be dictionary.')

    def tolist(self):
        """Output pulse envelope as a list of complex values

        Parameters:
            name (str): name of pulse

        Returns:
            list: complex pulse envelope at each sampling point
        Raises:
            QiskitError: when pulse envelope is not a number
        """

        samples = self.pulse(self.duration, **self._params)

        if any(abs(samples) > 1):
            warnings.warn("Pulse amplitude exceeds 1")
            _samples = np.where(abs(samples) > 1, samples/abs(samples), samples)
        else:
            _samples = samples

        return SamplePulse(_samples)
