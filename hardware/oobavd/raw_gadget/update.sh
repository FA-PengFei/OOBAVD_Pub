#!/bin/bash
# SPDX-License-Identifier: Apache-2.0

set -eux

REPO=https://git.kernel.org/pub/scm/linux/kernel/git/gregkh/usb.git/plain
BRANCH=usb-next

wget $REPO/drivers/usb/gadget/legacy/raw_gadget.c?h=$BRANCH -O raw_gadget.c
wget $REPO/include/uapi/linux/usb/raw_gadget.h?h=$BRANCH -O raw_gadget.h

git apply ./include.patch
