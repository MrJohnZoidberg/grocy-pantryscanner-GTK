# grocy-pantryscanner-GTK

## Installation
On a Raspberry Pi 3 Model B:
```bash
git clone https://github.com/MrJohnZoidberg/grocy-pantryscanner-GTK
cd grocy-pantryscanner-GTK
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Give normal user permissions for RPi backlight and USB for 4 Mic Array Board:
```bash
echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/99-backlight-permissions.rules
echo 'SUBSYSTEM=="usb",ATTRS{idVendor}=="2886", ATTRS{idProduct}=="0018",TAG+="uaccess"' | sudo tee -a /etc/udev/rules.d/99-usb-4mic-array-permissions.rules
```