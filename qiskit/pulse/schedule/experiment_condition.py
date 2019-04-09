# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
Configurations for pulse experiments.
"""
from typing import Dict

from qiskit.pulse.channels import OutputChannel


class UserLoDict:
    """Dictionary of user LO frequency by channel"""

    def __init__(self, user_lo_dic: Dict[OutputChannel, float] = None):
        self._user_lo_dic = {}
        if user_lo_dic:
            for channel, user_lo in user_lo_dic.items():
                # TODO: lo_range check
                self._user_lo_dic[channel] = user_lo

    def items(self):
        return self._user_lo_dic.items()
