<<<<<<< HEAD
import os
import shutil
import subprocess
import sys
from time import sleep

import magic
import usb.core
import usb.util
from detect import *

=======
>>>>>>> ac6e4a2dd26ed6a1ff9d224b0ca01a6d33efeb66


class find_class(object):
    def __init__(self, class_):
        self._class = class_

    def __call__(self, device):
        # first, let's check the device
        if device.bDeviceClass == self._class:
            return True
        # ok, transverse all devices to find an
        # interface that matches our class
        for cfg in device:
            # find_descriptor: what's it?
            intf = usb.util.find_descriptor(
                cfg,
                bInterfaceClass=self._class
            )
            if intf is not None:
                return True

        return False


#dev = usb.core.find(find_all=1, custom_match=find_class(8))
# for cfg in dev:
#    print(str(cfg.idVendor))
#    print(str(cfg.idProduct))
# for cfg in dev:
#    sys.stdout.write(str(cfg) + '\n')


def main():
    merged = False #Specify if running tow model or one model
    # initialize the model TODO: make it more efficient, just testing if it works rn
    classification_model = load_model()
    classification_doc_model = load_doc_model()
    #classification_merged_model = load_merged_model()

    devices_list = []
    emulated_list = []
    #comp_gadget = device()

    mounted_filepath = "/home/pi/mount"

    while True:
        # TODO: fix multiple devices
        devices_list = []
        dev = usb.core.find(find_all=1, custom_match=find_class(8))
        for cfg in dev:
            dev_idVendor = cfg.idVendor
            dev_idProduct = cfg.idProduct
            if f"{dev_idVendor}:{dev_idProduct}" not in devices_list:
                devices_list.append(
                    {"vendor": dev_idVendor, "product": dev_idProduct})
        # check for new devices
        for device_ in devices_list:
            if device_ not in emulated_list:
                print("attached")
                # TODO create img with same size as thumbdrive
                size = calculate_size()

                # mount thumbdrive
                mount(mounted_filepath)
                # init emulated device
                # comp_gadget.init(
                #    idVendor=hex(device_["vendor"]),
                #    idProduct=hex(device_["product"]),
                #    iSerialNumber="696969",
                #    iManufacturer="Jing Zhi",
                #    iProduct="Jing Zhis Pi").add_msd("/home/pi/oobavd/scripts/msd.img").start()
                emulated_list.append(device_)

                # enumerate through the files and start predict.
                files = get_filepaths(mounted_filepath)
                print(files)
                for file_loc in files:
                    file_type = magic.from_file(file_loc)
                    results = False

                    ##either go with merged model of sep models
                    image = convert_to_img(file_loc)
                    if file_type[:2] == "PE":
                        results = predict(classification_model, image)
                    elif "Microsoft Office" in file_type:
                        results = predict_doc(classification_doc_model, image)
                    
                    if results:
                        remove_file(file_loc, keep_copy=True)

                    print(file_loc + " - Malware: " + str(results))

                #sleep(1)
                #umount(mounted_filepath)
                sleep(1)
                usbproxy(0, 0)

        for emulated in emulated_list:
            if emulated not in devices_list:
                print("detached")
                # comp_gadget.remove()
                umount(mounted_filepath)
                emulated_list = []
        
        #print("loop")
        sleep(1)


def calculate_size():
    return 0


def mount(filepath):
    # TODO: mount with uuid
    partition = os.popen('blkid | grep /dev/sd').read()
    partition = partition.split(":")[0]
    if partition == "":
        partition = "/dev/sda1"
    # mount to filepath
    os.system(f"mount {partition} {filepath}")
    return


def umount(filepath):
    # TODO: mount with uuid
    partition = os.popen('blkid | grep /dev/sd').read()
    partition = partition.split(":")[0]
    if partition == "":
        partition = "/dev/sda1"
    # mount to filepath
    os.system(f"umount {partition}")
    return

# just yeet the files that have malware man yolo


def remove_file(filepath, keep_copy=False):
    if keep_copy:
        shutil.copy(filepath, '/home/pi/oobavd/samples')

    os.remove(filepath)
    #os.system(f"rm {filepath}")

#TODO: include vendor id and hardware id im abit too lazy right now
def usbproxy(vendor_id, product_id):
    #os.system("/home/pi/usb-proxy2/usb-proxy &")

    os.system("/home/pi/usb-proxy2/usb-proxy > /dev/null")
    #proc = subprocess.Popen(["/home/pi/usb-proxy2/usb-proxy"])




def get_filepaths(filepath):
    result = []
    for (root, dirs, files) in os.walk(filepath):
        for file in files:
            result.append(os.path.join(root, file))
    return result


if __name__ == "__main__":
    main()
