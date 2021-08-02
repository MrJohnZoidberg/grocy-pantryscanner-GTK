# grocy-pantryscanner-GTK

## Installation

```bash
git clone https://github.com/MrJohnZoidberg/grocy-pantryscanner-GTK
cd grocy-pantryscanner-GTK
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules
```