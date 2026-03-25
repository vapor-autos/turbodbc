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

  def _rx_cruise_enable_msg(self, enabled):
    return common.make_msg(1, 0x205, 1, dat=bytes([1 if enabled else 0]))

  def _rx_steer_feedback_msg(self, raw_steer):
    return common.make_msg(1, 0x208, 2, dat=int(raw_steer).to_bytes(2, byteorder="little", signed=True))

  def _rx_speed_msg(self, raw_speed):
    return common.make_msg(1, 0x209, 2, dat=int(raw_speed).to_bytes(2, byteorder="little", signed=False))

  def test_rx_hook(self):
    self.assertFalse(self.safety.get_controls_allowed())

    self.assertTrue(self._rx(self._rx_cruise_enable_msg(True)))
    self.assertTrue(self.safety.get_controls_allowed())

    self.safety.set_controls_allowed(False)
    self.assertTrue(self._rx(self._rx_steer_feedback_msg(1500)))
    self.assertTrue(self.safety.get_controls_allowed())

    self.safety.set_controls_allowed(False)
    self.assertTrue(self._rx(self._rx_speed_msg(0)))
    self.assertTrue(self.safety.get_controls_allowed())

  def test_tx_hook_whitelisted(self):
    self.safety.set_controls_allowed(False)
    self.assertTrue(self._tx(self._tx_steer_msg(90)))
    self.assertTrue(self._tx(self._tx_throttle_msg(0)))

  def test_tx_hook_blocks_non_whitelisted(self):
    self.assertFalse(self._tx(common.make_msg(1, 0x205, 1)))
    self.assertFalse(self._tx(common.make_msg(1, 0x209, 2)))


if __name__ == "__main__":
  unittest.main()
