#!/bin/bash
# SPDX-License-Identifier: Apache-2.0

set -eux

modprobe udc_core
insmod ./raw_gadget.ko
