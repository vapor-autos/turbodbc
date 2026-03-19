#!/usr/bin/env python3
import unittest

from opendbc.car.structs import CarParams
import opendbc.safety.tests.common as common
from opendbc.safety.tests.libsafety import libsafety_py
from opendbc.safety.tests.common import CANPackerSafety


class TestTurbo(common.SafetyTest):
  TX_MSGS = [[0x202, 1], [0x203, 1], [0x204, 1]]
  FWD_BUS_LOOKUP = {}

  def setUp(self):
    self.packer = CANPackerSafety("turbo_rc_car")
    self.safety = libsafety_py.libsafety
    self.safety.set_safety_hooks(CarParams.SafetyModel.turbo, 0)
    self.safety.init_tests()

  def _tx_steer_msg(self, steer_angle):
    values = {"STEER_ANGLE": steer_angle}
    return self.packer.make_can_msg_safety("STEER_CMD", 1, values)

  def _tx_throttle_msg(self, throttle):
    values = {"THROTTLE": throttle}
    return self.packer.make_can_msg_safety("THROTTLE_CMD", 1, values)

  def test_rx_hook(self):
    self.assertFalse(self.safety.get_controls_allowed())
    self.assertTrue(self._rx(common.make_msg(1, 0x265, 8)))
    self.assertTrue(self.safety.get_controls_allowed())

  def test_tx_hook_whitelisted(self):
    self.safety.set_controls_allowed(False)
    self.assertTrue(self._tx(self._tx_steer_msg(90)))
    self.assertTrue(self._tx(self._tx_throttle_msg(0)))


if __name__ == "__main__":
  unittest.main()
