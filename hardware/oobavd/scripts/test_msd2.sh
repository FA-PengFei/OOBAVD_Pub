#!/bin/sh

cd /sys/kernel/config/usb_gadget
mkdir -p pi2
cd pi2

echo 0xabcd > idVendor
echo 0x1234 > idProduct
echo 0x0100 > bcdDevice
echo 0x200 > bcdUSB

mkdir -p strings/0x409
echo "6969691" > strings/0x409/serialnumber
echo "Jing Zhi" > strings/0x409/manufacturer
echo "Jing Zhi's Second Pi" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo 0x80 > configs/c.1/bmAttributes
echo 250 > configs/c.1/MaxPower

#create functions
mkdir -p functions/mass_storage.usb0
echo 1 > functions/mass_storage.usb0/stall
echo 0 > functions/mass_storage.usb0/lun.0/cdrom
echo 0 > functions/mass_storage.usb0/lun.0/ro
echo 0 > functions/mass_storage.usb0/lun.0/nofua
#echo "JingDisk" > functions/mass_storage.usb0/iProduct
#echo 1234 > functions/mass_storage.usb0/idVendor
#echo 1234 > functions/mass_storage.usb0/idProduct
#echo "6969696969" > functions/mass_storage.usb0/iSerialNumber

#test mount second thumbdrive
#mkdir -p functions/mass_storage.usb1
#echo 1 > functions/mass_storage.usb1/stall
#echo 0 > functions/mass_storage.usb1/lun.0/cdrom
#echo 0 > functions/mass_storage.usb1/lun.0/ro
#echo 0 > functions/mass_storage.usb1/lun.0/nofua


echo /home/pi/oobavd/scripts/msd.img > functions/mass_storage.usb0/lun.0/file
#echo /home/pi/oobavd/scripts/msd.img > functions/mass_storage.usb1/lun.0/file
#echo /home/pi/oobavd/scripts/file > functions/mass_storage.usb0/lun.0/file
ln -s functions/mass_storage.usb0 configs/c.1/
#ln -s functions/mass_storage.usb1 configs/c.1/
udevadm settle -t 5 || :
ls /sys/class/udc > UDC