# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
Schedule.
"""
import logging
from copy import copy
from typing import List, Tuple

from qiskit.pulse.common.interfaces import ScheduleComponent
from qiskit.pulse.common.timeslots import TimeslotCollection
from qiskit.pulse.exceptions import PulseError

logger = logging.getLogger(__name__)


class Schedule(ScheduleComponent):
    """Immutable Schedule of instructions. The composite node of a schedule tree."""

    def __init__(self, *schedules, name: str = None, start_time: int = 0):
        """Create empty schedule.

        Args:
            name (str, optional): Name of this schedule. Defaults to None.
            start_time (int, optional): Begin time of this schedule. Defaults to 0.
        """
        self._name = name
        self._start_time = start_time
        self._occupancy = TimeslotCollection(timeslots=[])
        self._children = ()

    @property
    def name(self) -> str:
        """Name of this schedule."""
        return self._name

    @property
    def duration(self) -> int:
        return self.stop_time - self.start_time

    @property
    def occupancy(self) -> TimeslotCollection:
        return self._occupancy

    @property
    def start_time(self) -> int:
        return self._start_time

    @property
    def stop_time(self) -> int:
        return max([slot.interval.end for slot in self._occupancy.timeslots],
                   default=self._start_time)

    @property
    def children(self) -> Tuple[ScheduleComponent, ...]:
        return self._children

    def __add__(self, schedule: ScheduleComponent):
        return self.append(schedule)

    def __or__(self, schedule: ScheduleComponent):
        return self.insert(0, schedule)

    def __str__(self):
        # TODO: Handle schedule of schedules
        for child in self._children:
            if child.children:
                raise NotImplementedError("This version doesn't support schedule of schedules.")
        return '\n'.join([str(child) for child in self._children])

    def flat_instruction_sequence(self) -> List[ScheduleComponent]:
        """Return instruction sequence of this schedule.
        Each instruction has absolute start time.
        """
        if not self._children:  # empty schedule
            return []
        return [_ for _ in Schedule._flatten_generator(self, self.start_time)]

    @staticmethod
    def _flatten_generator(node: ScheduleComponent, time: int):
        if node.children:
            for child in node.children:
                yield from Schedule._flatten_generator(child, time + node.start_time)
        else:
            yield node.shifted(time)
