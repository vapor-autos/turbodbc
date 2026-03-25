from opendbc.can import CANPacker
from opendbc.car import Bus
from opendbc.car.interfaces import CarControllerBase
from opendbc.car.lateral import apply_std_steer_angle_limits
from opendbc.car.turbo.values import CarControllerParams


class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.main])
    self.apply_angle_last = 0.0

  def update(self, CC, CS, now_nanos):
    actuators = CC.actuators
    can_sends = []

    if CC.enabled:
      self.apply_angle_last = apply_std_steer_angle_limits(
        actuators.steeringAngleDeg,
        self.apply_angle_last,
        CS.out.vEgoRaw,
        CS.out.steeringAngleDeg,
        CC.latActive,
        CarControllerParams.ANGLE_LIMITS,
      )

      if self.frame % CarControllerParams.STEER_STEP == 0:
        steering_val = self.angle_to_servo(self.apply_angle_last)
        can_sends.append(self.packer.make_can_msg("STEER_CMD", 1, {"STEER_ANGLE": steering_val}))

      throttle_val = self.normalize_accel(actuators.accel)
      can_sends.append(self.packer.make_can_msg("THROTTLE_CMD", 1, {"THROTTLE": throttle_val}))

      if CC.leftBlinker:
        can_sends.append(self.packer.make_can_msg("TOGGLE_HEADLIGHTS", 1, {"HEADLIGHTS_TOGGLE": 1}))
      elif CC.rightBlinker:
        can_sends.append(self.packer.make_can_msg("TOGGLE_HEADLIGHTS", 1, {"HEADLIGHTS_TOGGLE": 0}))

    new_actuators = actuators.as_builder()
    new_actuators.steeringAngleDeg = self.apply_angle_last
    self.frame += 1

    return new_actuators, can_sends

  def angle_to_servo(self, steering_angle_deg):
    return int(steering_angle_deg * -100.0)

  def normalize_accel(self, accel):
    return int(accel * 2500)
