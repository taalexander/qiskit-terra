# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""Test for the CmdDef object."""

import numpy as np

from qiskit.test import QiskitTestCase
from qiskit.test.mock import FakeProvider
from qiskit.pulse import (CmdDef, SamplePulse, Schedule, DeviceSpecification,
                          PulseError, PersistentValue)


class TestCmdDef(QiskitTestCase):
    """Test CmdDef methods."""

    def setUp(self):
        self.provider = FakeProvider()
        self.backend = self.provider.get_backend('fake_openpulse_2q')
        self.device = DeviceSpecification.create_from(self.backend)

    def test_get_backend(self):
        """Test that backend is fetchable with cmd def present."""

    def test_init(self):
        """Test `init`, `has`."""
        sched = Schedule()
        sched.append(SamplePulse(np.ones(5))(self.device.q[0].drive))
        cmd_def = CmdDef({('tmp', 0): sched})
        self.assertTrue(cmd_def.has('tmp', 0))

    def test_add(self):
        """Test `add`, `has`, `get`, `cmd_types`."""
        sched = Schedule()
        sched.append(SamplePulse(np.ones(5))(self.device.q[0].drive))
        cmd_def = CmdDef()
        cmd_def.add('tmp', 0, sched)
        self.assertEqual(sched.instructions, cmd_def.get('tmp', (0,)).instructions)

        self.assertIn('tmp', cmd_def.cmd_types())

    def test_pop(self):
        """Test pop with default."""
        sched = Schedule()
        sched.append(SamplePulse(np.ones(5))(self.device.q[0].drive))
        cmd_def = CmdDef()
        cmd_def.add('tmp', 0, sched)
        cmd_def.pop('tmp', 0)
        self.assertFalse(cmd_def.has('tmp', 0))

        with self.assertRaises(PulseError):
            cmd_def.pop('not_there', (0,))

    def test_repr(self):
        """Test repr"""
        sched = Schedule()
        sched.append(SamplePulse(np.ones(5))(self.device.q[0].drive))
        cmd_def = CmdDef({('tmp', 0): sched})
        repr(cmd_def)

    def test_build_cmd_def(self):
        """Test building of parameterized cmd_def"""
        defaults = self.backend.defaults()
        cmd_def = defaults.build_cmd_def()

        cx_pv = cmd_def.get('cx', (0, 1), P2=0)
        pv_found = False
        for _, instr in cx_pv.instructions:
            cmd = instr.command
            if isinstance(cmd, PersistentValue):
                self.assertEqual(cmd.value, 1)
                pv_found = True
        self.assertTrue(pv_found)

        u1_minus_pi = cmd_def.get('u1', 0, P1=1)
        fc_cmd = u1_minus_pi.instructions[0][-1].command
        self.assertEqual(fc_cmd.phase, np.pi)
