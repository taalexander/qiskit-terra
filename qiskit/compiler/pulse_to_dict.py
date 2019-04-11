# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""Helper class to assemble pulse instruction to PulseQobjInstruction."""

from qiskit.pulse import commands
from qiskit.qobj import QobjMeasurementOption

from functools import wraps


def bind_instruction(type_instruction):
    def _wrapper(convert_func):
        def _decorated_converter(instruction):
            if isinstance(instruction, type_instruction):
                return convert_func(instruction)
            else:
                pass
        return _decorated_converter
    return _wrapper


class SuperConverter:

    def __init__(self, qobj_model, meas_level=2):
        """Create new converter.

        Args:
             qobj_model (QobjInstruction): marshmallow model to serialize to object.
             meas_level (int): Level of measurement.
        """
        self.qobj_model = qobj_model
        self.meas_level = meas_level

    def __call__(self, *args, **kwargs):
        pass

    @bind_instruction(commands.AcquireInstruction)
    def _convert_acquire(self, instruction):
        """Return Acquire dict for Qobj.

        Args:
            instruction (AcquireInstruction): acquire instruction.
        Returns:
            dict: Dictionary of required parameters.
        """
        command_dict = {
            'name': 'acquire',
            't0': instruction.begin_time,
            'duration': instruction.duration,
            'qubits': [q.index for q in instruction.qubits],
            'memory_slot': [m.index for m in instruction.mem_slots]
        }
        if self.meas_level == 2:
            # setup discriminators
            if instruction.command.discriminator:
                command_dict.update({
                    'discriminators': [
                        QobjMeasurementOption(
                            name=instruction.command.discriminator.name,
                            params=instruction.command.discriminator.params)
                    ]
                })
            else:
                command_dict.update({
                    'discriminators': []
                })
            # setup register_slots
            command_dict.update({
                'register_slot': [regs.index for regs in instruction.reg_slots]
            })
        if self.meas_level >= 1:
            # setup kernels
            if instruction.command.kernel:
                command_dict.update({
                    'kernels': [
                        QobjMeasurementOption(
                            name=instruction.command.kernel.name,
                            params=instruction.command.kernel.params)
                    ]
                })
            else:
                command_dict.update({
                    'kernels': []
                })
        return self.qobj_model(**command_dict)

    @bind_instruction(commands.FrameChangeInstruction)
    def _convert_frame_change(self, instruction):
        """Return FrameChange dict for Qobj.

        Args:
            instruction (FrameChangeInstruction): frame change instruction.
        Returns:
            dict: Dictionary of required parameters.
        """
        command_dict = {
            'name': 'fc',
            't0': instruction.begin_time,
            'ch': instruction.channel.name,
            'phase': instruction.command.phase
        }
        return self.qobj_model(**command_dict)

    @bind_instruction(commands.PersistentValueInstruction)
    def _convert_persistent_value(self, instruction):
        """Return PersistentValue dict for Qobj.

        Args:
            instruction (PersistentValueInstruction): persistent value instruction.
        Returns:
            dict: Dictionary of required parameters.
        """
        command_dict = {
            'name': 'pv',
            't0': instruction.begin_time,
            'ch': instruction.channel.name,
            'val': instruction.command.value
        }
        return self.qobj_model(**command_dict)

    @bind_instruction(commands.DriveInstruction)
    def _convert_drive(self, instruction):
        """Return Drive dict for Qobj.

        Args:
            instruction (DriveInstruction): drive instruction.
        Returns:
            dict: Dictionary of required parameters.
        """
        command_dict = {
            'name': instruction.command.name,
            't0': instruction.begin_time,
            'ch': instruction.channel.name
        }
        return self.qobj_model(**command_dict)

    @bind_instruction(commands.Snapshot)
    def _convert_snapshot(self, instruction):
        """Return SnapShot dict for Qobj.

        Args:
            instruction (Snapshot): snapshot instruction.
        Returns:
            dict: Dictionary of required parameters.
        """
        command_dict = {
            'name': 'snapshot',
            't0': instruction.begin_time,
            'label': instruction.label,
            'type': instruction.type
        }
        return self.qobj_model(**command_dict)
