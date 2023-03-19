#!/bin/sh

cd /sys/kernel/config/usb_gadget

echo "" > UDC

#rm -rf pi
#udevadm settle -t 5 || :
#ls /sys/class/udc > UDC