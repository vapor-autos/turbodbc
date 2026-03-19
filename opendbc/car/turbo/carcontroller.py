from opendbc.can import CANPacker
from opendbc.car import Bus
from opendbc.car.interfaces import CarControllerBase


class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.main])

  def update(self, CC, CS, now_nanos):
    new_actuators = CC.actuators.as_builder()
    can_sends = []

    if CC.enabled:
      steering_val = self.normalize_steer(CC.actuators.torque)
      can_sends.append(self.packer.make_can_msg("STEER_CMD", 1, {"STEER_ANGLE": steering_val}))

      throttle_val = self.normalize_accel(CC.actuators.accel)
      can_sends.append(self.packer.make_can_msg("THROTTLE_CMD", 1, {"THROTTLE": throttle_val}))

      if CC.leftBlinker:
        can_sends.append(self.packer.make_can_msg("TOGGLE_HEADLIGHTS", 1, {"HEADLIGHTS_TOGGLE": 1}))
      elif CC.rightBlinker:
        can_sends.append(self.packer.make_can_msg("TOGGLE_HEADLIGHTS", 1, {"HEADLIGHTS_TOGGLE": 0}))

    return new_actuators, can_sends

  def normalize_accel(self, accel):
    # Normalize accel from [-4.0, 4.0] to [-100, 100]
    return int(accel * 25)

  def normalize_steer(self, steer):
    # Normalize steer from [-1.0, 1.0] to [60, 120], sign flipped for platform convention
    return int(90 + steer * -30)
