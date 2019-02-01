# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.
# pylint: disable=invalid-name,missing-docstring,missing-param-doc

"""
Base class of pulse commands
"""

import uuid


class PulseCommand:
    """Base class of pulse commands"""

    def __init__(self, duration):
        """create new pulse commands

        Parameters:
            duration (int): duration of pulse
        """

        self.duration = duration
        self.id = str(uuid.uuid4())
