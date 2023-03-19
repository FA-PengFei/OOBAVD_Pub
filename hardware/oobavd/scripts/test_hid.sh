#!/bin/sh

#create gadgets
cd /sys/kernel/config/usb_gadget
mkdir -p pi
cd pi

echo 0x1d6b > idVendor
echo 0x0104 > idProduct
echo 0x0100 > bcdDevice
echo 0x200 > bcdUSB

mkdir -p strings/0x409
echo "696969" > strings/0x409/serialnumber
echo "Jing Zhi" > strings/0x409/manufacturer
echo "Jing Zhis Pi" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo 0x80 > configs/c.1/bmAttributes
echo 250 > configs/c.1/MaxPower

mkdir -p functions/hid.usb0
mkdir configs/c.1
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc
echo 250 > configs/c.1/MaxPower
echo 0x80 > configs/c.1/bmAttributes #  USB_OTG_SRP | USB_OTG_HNP
ln -s functions/hid.usb0 configs/c.1/

#mount device
#rmmod g_ether
ls /sys/class/udc > UDC