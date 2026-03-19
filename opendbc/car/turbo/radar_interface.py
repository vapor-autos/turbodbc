from opendbc.car.interfaces import RadarInterfaceBase


class RadarInterface(RadarInterfaceBase):
  # Turbo has no separate radar CAN integration; use the base no-radar behavior.
  pass
