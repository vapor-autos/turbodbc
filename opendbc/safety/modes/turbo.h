#pragma once

#include "opendbc/safety/declarations.h"

static void turbo_rx_hook(const CANPacket_t *msg) {
  const uint32_t addr = msg->addr;
  const bool is_cruise_msg = (addr == 0x205U);
  const bool is_steer_msg = (addr == 0x208U);
  const bool is_speed_msg = (addr == 0x209U);

  if (is_cruise_msg || is_steer_msg || is_speed_msg) {
    controls_allowed = true;
  }
}

static bool turbo_tx_hook(const CANPacket_t *msg) {
  SAFETY_UNUSED(msg);

  // By design for RC operation: controls are always allowed so teleop and
  // self-drive can hand off without a separate engage gate.
  // This intentionally differs from normal on-road safety semantics.
  controls_allowed = true;
  return true;
}

static safety_config turbo_init(uint16_t param) {
  static RxCheck turbo_rx_checks[] = {
    {.msg = {{0x205, 1, 1, 25U, .ignore_checksum = true, .ignore_counter = true, .ignore_quality_flag = true}, { 0 }, { 0 }}},
    {.msg = {{0x208, 1, 2, 25U, .ignore_checksum = true, .ignore_counter = true, .ignore_quality_flag = true}, { 0 }, { 0 }}},
    {.msg = {{0x209, 1, 2, 25U, .ignore_checksum = true, .ignore_counter = true, .ignore_quality_flag = true}, { 0 }, { 0 }}},
  };

  static const CanMsg TURBO_TX_MSGS[] = {
    {0x202, 1, 2, .check_relay = false},  // steer
    {0x203, 1, 2, .check_relay = false},  // throttle
    {0x204, 1, 2, .check_relay = false},  // headlights
  };

  SAFETY_UNUSED(param);
  safety_config ret = BUILD_SAFETY_CFG(turbo_rx_checks, TURBO_TX_MSGS);
  ret.disable_forwarding = true;
  return ret;
}

const safety_hooks turbo_hooks = {
  .init = turbo_init,
  .rx = turbo_rx_hook,
  .tx = turbo_tx_hook,
};
