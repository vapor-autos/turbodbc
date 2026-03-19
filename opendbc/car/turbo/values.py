from opendbc.car import Bus, CarSpecs, PlatformConfig, Platforms
from opendbc.car.docs_definitions import CarDocs, SupportType
from opendbc.car.lateral import AngleSteeringLimits

TYPHON_1_8_3S_SPECS = CarSpecs(
  mass=9,
  wheelbase=0.3302,
  steerRatio=180 / 30 * 3,
)

class CarControllerParams:
  ANGLE_LIMITS: AngleSteeringLimits = AngleSteeringLimits(
    180,
    ([0., 5., 25.], [40.0, 24.0, 3.2]),
    ([0., 5., 25.], [80.0, 32.0, 4.8]),
  )
  STEER_STEP = 2

class CAR(Platforms):
  TURBO_RC_CAR = PlatformConfig(
    [CarDocs("turbo rc car", package="All", support_type=SupportType.CUSTOM, support_link="#community")],
    TYPHON_1_8_3S_SPECS,
    {Bus.main: 'turbo_rc_car'},
  )

DBC = CAR.create_dbc_map()
