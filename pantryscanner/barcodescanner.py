import threading

import RPi.GPIO as GPIO
from evdev import InputDevice, ecodes, categorize
import pyglet  # sudo apt install gstreamer1.0-python3-plugin-loader
import time
import requests

CODE_MAP_CHAR = {
    'KEY_0': "0",
    'KEY_1': "1",
    'KEY_2': "2",
    'KEY_3': "3",
    'KEY_4': "4",
    'KEY_5': "5",
    'KEY_6': "6",
    'KEY_7': "7",
    'KEY_8': "8",
    'KEY_9': "9",
    'KEY_KP0': "0",
    'KEY_KP1': "1",
    'KEY_KP2': "2",
    'KEY_KP3': "3",
    'KEY_KP4': "4",
    'KEY_KP5': "5",
    'KEY_KP6': "6",
    'KEY_KP7': "7",
    'KEY_KP8': "8",
    'KEY_KP9': "9",
    'KEY_NUMERIC_0': "0",
    'KEY_NUMERIC_1': "1",
    'KEY_NUMERIC_2': "2",
    'KEY_NUMERIC_3': "3",
    'KEY_NUMERIC_4': "4",
    'KEY_NUMERIC_5': "5",
    'KEY_NUMERIC_6': "6",
    'KEY_NUMERIC_7': "7",
    'KEY_NUMERIC_8': "8",
    'KEY_NUMERIC_9': "9",
    'KEY_A': "A",
    'KEY_B': "B",
    'KEY_C': "C",
    'KEY_D': "D",
    'KEY_E': "E",
    'KEY_F': "F",
    'KEY_G': "G",
    'KEY_H': "H",
    'KEY_I': "I",
    'KEY_J': "J",
    'KEY_K': "K",
    'KEY_L': "L",
    'KEY_M': "M",
    'KEY_N': "N",
    'KEY_O': "O",
    'KEY_P': "P",
    'KEY_Q': "Q",
    'KEY_R': "R",
    'KEY_S': "S",
    'KEY_T': "T",
    'KEY_U': "U",
    'KEY_V': "V",
    'KEY_W': "W",
    'KEY_X': "X",
    'KEY_Y': "Y",
    'KEY_Z': "Z",
    'KEY_DOT': ".",
    'KEY_MINUS': "-"
}


class BarcodeScanner:

    def __init__(self, pantryscanner):
        self._pantryscanner = pantryscanner
        self._bb_api_url = self._pantryscanner.get_config_value('barcodebuddy', 'bb_server_url') + "api/"
        self._bb_api_key = self._pantryscanner.get_config_value('barcodebuddy', 'bb_api_key')
        self.event_id = self._pantryscanner.get_config_value('barcodebuddy', 'screen', 'scanner_dev_event_number')
        self._gpio_relais: int = self._pantryscanner.get_config_value("scanner", "gpio_relais")
        self.sound = pyglet.media.load("resources/beep-07a.wav", streaming=False)
        GPIO.setup(self._gpio_relais, GPIO.OUT)
        self.thread = None
        self.terminate_thread = False
        self.timer_scanner_pause = None
        self.on()

    def on(self):
        GPIO.output(self._gpio_relais, GPIO.HIGH)
        self.terminate_thread = False
        self.thread = threading.Thread(target=self.read_input)
        self.thread.start()

    def off(self):
        GPIO.output(self._gpio_relais, GPIO.LOW)
        if self.timer_scanner_pause and self.timer_scanner_pause.is_alive():
            self.timer_scanner_pause.cancel()
        self.terminate_thread = True
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def read_input(self):
        while not self.terminate_thread:
            try:
                device = InputDevice('/dev/input/event{}'.format(self.event_id))
                device.grab()

                data = ""
                for event in device.read_loop():
                    if event.type == ecodes.EV_KEY and not self.terminate_thread:
                        e = categorize(event)
                        if e.keystate == e.key_up:
                            if e.keycode == "KEY_ENTER":
                                self.sound.play()
                                self.off()
                                print("Sending :" + data)
                                requests.get(self._bb_api_url + 'action/scan?apikey=' + self._bb_api_key
                                             + '&add=' + data)
                                data = ""
                                self.timer_scanner_pause = threading.Timer(1, self.on)
                                self.timer_scanner_pause.start()
                            else:
                                data += self.parse_key_to_char(e.keycode)
            except OSError:
                time.sleep(0.5)

    @staticmethod
    def parse_key_to_char(val):
        return CODE_MAP_CHAR[val] if val in CODE_MAP_CHAR else ""
