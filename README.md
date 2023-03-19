# Out-Of-Band Anti-Virus Dock (OOBAVD)

*OOBAVD is created by [@yupengfei](https://github.com/FA-PengFei), [@zhangbosen](https://github.com/duemaster), [@tanjingzhi](https://github.com/jeijii), [@howardyang](https://github.com/reedless) and [@winstonho]()*

*OOBAVD is an experimental proof of concept and not ready for production use in its current form.*

**Contents**

1. [The Motivation](#the-motivation)

   ​	[How does OOVBAVD work?](#how-does-oobavd-works)

   ​	[OOBAVD's key features](#key-features)

2. [The Components | The magic behind OOBAVD](#the-components-of-oobavd)

   ​	[Out-Of-Band & Quarantine](#1-out-of-band--quarantine)

   ​	[Fighting Malware, One Neuron at a time](#2-fighting-malware-one-neuron-at-a-time)

3. [Setting up OOBAVD](#setting-up-oobavd)

   ​	[Requirements](#requirements)

   ​	[Installation and Usage](#installation-and-usage)

4. [Disclaimers & Other Considerations](#disclaimers--other-considerations)

5. [Licensing](#licensing)



# The Motivation

USB-based attacks account for more than [52%](https://gcn.com/cybersecurity/2022/08/more-half-ot-cyber-threats-used-usb-drives-report-finds/376142/) of all cybersecurity attacks on Operational Technology (OT) systems in the Industrial Control Systems (ICS) industry. The discovery of Stuxnet in 2015 served as a stark reminder that even air-gapped computers, which were previously thought to be impervious to cyber attacks, are vulnerable. These systems are commonly found in secure military organizations or Supervisory Control and Data Acquisition (SCADA) systems. The societal impact of such attacks can be enormous. The Stuxnet attack, for example, used USB autorun features to spread and cause significant damage to Iran's nuclear programs and facilities.

While air-gapped systems are considered "secure," they are inconvenient for computer operators, especially when performing updates and transferring data, which frequently necessitate the use of a mobile storage device, such as a USB stick. Unfortunately, this introduces a flaw into air-gapped systems, making them vulnerable to computer viruses and malware. Furthermore, adding new peripherals such as keyboards and mice to these systems may allow BadUSB attacks to be carried out on the air-gapped system as well.

OOBAVD is a solution to close this gap. OOBAVD serves as an intermidary between the air gapped system and different USB devices, it scans and block any detected malicious files from showing up on the air gapped system. In addition, malware is capable of attacking commercial software-based antivirus programs on the host machine by blocking, corrupting, and replacing the antivirus core files, rendering it incapable of functioning normally. This can effectively make the antivirus useless in defending against malware attacks. OOBAVD being out of band in the transfer process, would be able to mitigate against this risk.

OOBAVD is designed to have minimum software pre-installed unlike air gapped computers, so as to reduce the attack surface area for it to be infected. As an added protection mechanism, OOBAVD can also be wiped clean and flashed before connecting to new air gapped computers removing any persistent malware that even manages to infect OOBAVD.

 In short, OOBAVD is designed to address the following pain points: 

| Pain point | OOBAVD Feature | 
|---|----|
| Operator needs to remember to scan all files on the USB device before/after connecting to the system | OOBAVD implemented On-The-Fly live scanning of files as USB devices are plugged in | 
| It is difficult to update antivirus definitions on air gapped systems | OOBAVD is able to go into a "disarmed" mode, allowing it to be accessed and patched without the need to access these air gapped systems | 




### How does OOBAVD work?

OOBAVD runs out-of-the-box with two key components.
The protected resource can be customised by making a deployment change within the setup.

<p align="center">
  <img src="/images/Architecture.png"/>
   </br>
   <i>High level architecture of OOBAVD</i>
</p>

### Key Benefits
   
OOBAVD was engineered with the following key user benefits in mind:

#### **1. Additional layer of defense**
By acting as an intermediary, OOBAVD adds an extra layer of security to the computer it is protecting. It makes infecting the protected resource even more difficult because the malware must first infect OOBAVD. Furthermore, OOBAVD is configured with minimal pre-installed software, which reduces its own attack surface even further.

#### **2. Simplicity and Convenience**

OOBAVD was designed to be simple and convenient to operate. By having a clunky operation, it is likely that the operator will take shortcuts when transfering data. Hence it is vital that security measures make it as simple as possible for the operator to use, to ensure it is actually being used, and for security to be ensured for the protected resource.

<p align="center">
  <img src="/images/Detection.gif" width="600" height="375"/>
  <br/>
  <i>OOBAVD in action: When a USB flash drive is plugged in, its files are converted to byteplot representation, then sent to the CNN model to be classified.  </i>
</p>


# The Components of OOBAVD 

### 1. Out-of-Band & Quarantine
> *No malware will be make it through!*

OOBAVD operates via USB emulation to remain completely out-of-band (OOB). It's worth noting that the concept of OOB in OOBAVD differs somewhat from OOB in networking terms. In this context, OOB refers to the fact that the protected resource is incapable of detecting the presence of OOBAVD, and all communication between the resource and OOBAVD is limited to USB protocols. This approach significantly reduces the attack surface, essentially eliminating the malware's ability to bring down the protected resource's antivirus mentioned in the earlier section.

#### USB-Proxy

OOBAVD has gone through several iterations, with the current implementation determining that USB-Proxy is the most effective way to keep the system out of band. USB-Proxy allows for low-level control over the gadget's communication process. it was used after the enumeration of the mass storage device by the classification model. This allows for OOBAVD to act as a proxy for the mass storage device. There would be no mention of OOBAVD at all to the host, providing a true out of band experience

On the other hand, USB-Proxy adds additional performance overhead. In the our next update, we are considering developing a custom USB protocol that will streamline the process and may even include stream scanning to further enhance OOBAVD's capabilities.

#### Welcome to the malware jail

Our current version of OOBAVD includes the ability to quarantine malware files rather than deleting them immediately. This decision was made to make possible digital forensics work on the identified malware easier. We intend to include a feature in the next update that will allow users to disable this option if they prefer to have malware files deleted completely.

### 2. Fighting Malware, One Neuron at a time
> *Who needs manual when we can go NEURAL*

Instead of relying on hand-crafted features which require manual analysis and updating to detect malware, OOBAVD leverages the generalization power of CNNs to detect visual similarities in the byteplot images of malware variants belonging to the same family. This allows for a high confidence in detecting novel malware, even when the model is encountering it for the first time.

To achieve this, we gathered a collection of malicious and non-malicious executables from various public datasets, converted them to byteplot images, and experimented with a variety of model architectures to find one that suits our requirements the best. Even without any significant changes to the architectures, we were able to achieve an accuracy of over 95% in the following models which were also chosen for their small sizes and low latency:

Model | Link
--- | ---
EfficientNetV2-S | https://arxiv.org/abs/2104.00298
RegNetY_3.2GF | https://arxiv.org/abs/2003.13678
Densenet-201 | https://arxiv.org/abs/1608.06993
MNASNet with depth multiplier of 1.3 | https://arxiv.org/pdf/1807.11626.pdf
ShuffleNetV2 with 2.0x output channels | https://arxiv.org/abs/1807.11164
MobileNetV3-L | https://arxiv.org/abs/1905.02244

Users could select the models they are most comfortable with by loading it into OOBAVD. Pre-trained weights can be found [here](https://drive.google.com/drive/folders/1gE7ynbUyA5xEkjt0EQ6RE0bceo2dJRum?usp=sharing)

#### Performance

Model | Accuracy | Size (MB)
--- | --- | --- 
EfficientNetV2-S | 96% | 84.8
RegNetY_3.2GF | 95% | 76.4
Densenet-201 | 95% | 79.5
MNASNet | 95% | 24.8
ShuffleNetV2 | 95% | 29.1
MobileNetV3-L | 95% | 21.6

Though the results on our curated dataset are promising, it is important to note that past performance is not indicative of future results, and that it is important for users to prevent model degradation through model retraining. Upon first use, it can also be helpful to fine-tune the model to any specific threats that the user might wish to focus on.


### Sample Usage Scenarios
1. Airgapped systems that necessitates manual updates of files, tools, and system software via USB-based devices.
2. Any organization that wants to increase security when its employees connect USB devices.

## Setting up OOBAVD

### Requirements
OOBAVD requires a device with a USB OTG port for USB proxy to work.

Tested Hardware 
1. Raspberry Pi 4 Model B 


#### ML Component 
1. Python
2. Numpy
2. Pandas
3. PyTorch
3. FastAI

#### USB Proxy
1. [USB Raw Gadget](https://github.com/xairy/raw-gadget)
2. [USB-Proxy](https://github.com/AristoChen/usb-proxy)
3. [PyUSB](https://github.com/pyusb/pyusb)



### Installation and Usage
Install the required libraries.
```bash
sudo apt install libusb-1.0-0-dev libjsoncpp-dev
```

Install the required python libraries.
```bash
pip install -r requirements.txt
```

Create a systemd service for OOBAVD.
```bash
cp oobavd.service /etc/systemd/service/oobavd.service

sudo systemctl daemon-reload

sudo systemctl enable oobavd.service
```


## Disclaimers & Other Considerations

OOBAVD is a W.I.P, Open source project, functions and features may change from patch to patch.
If you are interested to contribute, please feel free to create an issue or pull request!


## Licensing

#### License

[MIT License](/LICENSE) 
