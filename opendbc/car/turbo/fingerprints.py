""" AUTO-FORMATTED USING opendbc/car/debug/format_fingerprints.py, EDIT STRUCTURE THERE."""
from opendbc.car.structs import CarParams
from opendbc.car.turbo.values import CAR

Ecu = CarParams.Ecu

# debug ecu fw version is the git hash of the firmware


FINGERPRINTS = {
  CAR.TURBO_RC_CAR: [{
    613: 8,
    614: 8,
    615: 8,
  }],
}

FW_VERSIONS = {
  CAR.TURBO_RC_CAR: {
    (Ecu.engine, 0x722, None): [
      b'0.0.01',
      b'0.3.00a',
      b'02/27/2022',
    ],
    (Ecu.debug, 0x723, None): [
      b'put_git_hash_here',
    ],
  },
}
