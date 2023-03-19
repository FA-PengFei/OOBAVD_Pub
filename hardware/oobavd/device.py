import os


class device:
    def __init__(self):
        self.device_name = "pi"
        self.gadget_count = 0
        self.idVendor = ""
        self.idProduct = ""
        self.bcdDevice = ""
        self.bcdUSB = ""
        self.iSerialNumber = ""
        self.iManufacturer = ""
        self.iProduct = ""

    """
        Initialize and create the usb device.
    """

    def init(self, **args):
        self.idVendor = args["idVendor"]
        self.idProduct = args["idProduct"]

        if "bcdDevice" in args:
            self.bcdDevice = args["bcdDevice"]  # 0x0100
        else:
            self.bcdDevice = 0x0100

        if "bcdUSB" in args:
            self.bcdUSB = args["bcdUSB"]  # 0x200
        else:
            self.bcdUSB = 0x200

        # TODO: provide defaults
        self.iSerialNumber = args["iSerialNumber"]
        self.iManufacturer = args["iManufacturer"]
        self.iProduct = args["iProduct"]
        path = "/sys/kernel/config/usb_gadget"
        os.chdir(path)

        if os.path.exists(f"{path}/{self.device_name}") is False:
            os.mkdir(self.device_name)

        os.chdir(self.device_name)

        os.system(f'echo {self.idProduct} > idProduct')
        os.system(f'echo {self.idVendor} > idVendor')
        os.system(f'echo {self.bcdDevice} > bcdDevice')
        os.system(f'echo {self.bcdUSB} > bcdUSB')
        # print(os.getcwd())
        strings_path = "strings/0x409"
        os.makedirs(strings_path, exist_ok=True)
        os.system(f'echo {self.iSerialNumber} > {strings_path}/serialnumber')
        os.system(f'echo {self.iManufacturer} > {strings_path}/manufacturer')
        os.system(f'echo {self.iProduct} > {strings_path}/product')

        os.makedirs("configs/c.1/strings/0x409", exist_ok=True)
        os.system(f'echo 0x80 > configs/c.1/bmAttributes')
        os.system(f"echo 250 > configs/c.1/MaxPower")

        return self

    """
        Start the device, must have functions before starting.
    """

    def start(self):
        os.system("ls /sys/class/udc > UDC")

    """
        Add a mass storage device gadget
    """

    def add_msd(self, path_to_image):
        # TODO: check if in the correct working directory.
        gadget_path = f'functions/mass_storage.usb{self.gadget_count}'
        os.makedirs(gadget_path, exist_ok=True)
        os.system(f'echo 1 > {gadget_path}/stall')
        os.system(f'echo 0 > {gadget_path}/lun.0/cdrom')
        os.system(f'echo 0 > {gadget_path}/lun.0/ro')
        os.system(f'echo 0 > {gadget_path}/lun.0/nofua')
        os.system(f'echo "{path_to_image}" > {gadget_path}/lun.0/file')
        os.system(f'ln -s {gadget_path} configs/c.1/')

        # self.gadget_count += 1 //shitty code
        return self

    def remove(self):
        os.system(' echo "" > UDC')
