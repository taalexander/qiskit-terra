# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
Instruction = Leaf node of schedule.
"""
import logging
from typing import Tuple, List, Iterable

from qiskit.pulse.exceptions import PulseError
from qiskit.pulse.channels import Channel
from qiskit.pulse.interfaces import ScheduleComponent
from qiskit.pulse.schedule import Schedule
from qiskit.pulse.timeslots import Interval, Timeslot, TimeslotCollection

logger = logging.getLogger(__name__)

# pylint: disable=missing-return-doc


class Instruction(Schedule):
    """An abstract leaf class for Schedule nodes."""

    def __init__(self, command, *channels: List[Channel],
                 timeslots: TimeslotCollection = None, name=None):
        self._command = command
        self._name = name if name else self._command.name
        duration = command.duration

        if timeslots and channels:
            raise PulseError('Channels and timeslots may not both be supplied.')

        if not timeslots:
            self._timeslots = TimeslotCollection(*(Timeslot(Interval(0, duration), channel)
                                                   for channel in channels))
        else:
            self._timeslots = timeslots

    @property
    def name(self) -> str:
        return self._name

    @property
    def timeslots(self) -> TimeslotCollection:
        return self._timeslots

    @property
    def command(self):
        """Acquire command."""
        return self._command

    @property
    def children(self) -> Tuple[ScheduleComponent]:
        """Instruction has no child nodes. """
        return ()

    def flatten(self, time: int = 0) -> Iterable[Tuple[int, ScheduleComponent]]:
        """Iterable for flattening Schedule tree.

        Args:
            time: Shifted time of this node due to parent

        Yields:
            Tuple[int, ScheduleComponent]: Tuple containing time `ScheduleComponent` starts
                at and the flattened `ScheduleComponent`.
        """
        yield (time, self)

    def __repr__(self):
        return "Instruction(%s -> %s)" % (self.command, self.channels)
