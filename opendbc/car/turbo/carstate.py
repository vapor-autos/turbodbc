from opendbc.can import CANParser
from opendbc.car import Bus, structs
from opendbc.car.interfaces import CarStateBase
from opendbc.car.turbo.values import DBC


class CarState(CarStateBase):
  def update(self, can_parsers) -> structs.CarState:
    cp = can_parsers[Bus.main]
    ret = structs.CarState()
    ret.cruiseState.enabled = cp.vl["CRUISE_ENABLE"]["ENABLE"] == 1
    ret.cruiseState.available = True
    ret.gearShifter = structs.CarState.GearShifter.drive
    ret.vEgoRaw = cp.vl["SPEED_16"]["SPEED_16"] / 100.0
    ret.vEgo = ret.vEgoRaw
    ret.standstill = ret.vEgoRaw < 0.01
    ret.steeringAngleDeg = cp.vl["STEER_16"]["STEER_16"] / -100.0
    print(f"[turbo state] cruise={ret.cruiseState.enabled} vEgo={ret.vEgoRaw:.2f} raw_steer_fb={cp.vl['STEER_16']['STEER_16']} steer_deg={ret.steeringAngleDeg:.2f}")
    return ret

  @staticmethod
  def get_can_parsers(CP):
    messages = [
      ("CRUISE_ENABLE", 25),
      ("STEER_16", 25),
      ("SPEED_16", 25),
    ]
    return {Bus.main: CANParser(DBC[CP.carFingerprint][Bus.main], messages, 1)}
