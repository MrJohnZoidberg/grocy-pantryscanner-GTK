from . import grocy
from . import displaybacklight
from . import activitydetection_voice
from . import activitydetection_motion
from . import barcodescanner
from . import server
from . import speechrecognition
import RPi.GPIO as GPIO
import webbrowser
import os
import time
import signal
import sys


class PantryScanner:

    def __init__(self, config, config_default):
        GPIO.setmode(GPIO.BCM)
        self._config = config
        self._config_default = config_default
        self._grocy = grocy.Grocy(self)
        self._backlight = displaybacklight.DisplayBacklight()
        self._scanner = barcodescanner.BarcodeScanner(self)
        self._activitydetection = self.setup_activity_detection()
        self._server = server.Server(self)
        self._speechrecognition = speechrecognition.SpeechRecognition(self)
        signal.signal(signal.SIGINT, self.stop)

    def start(self):
        if self.get_config_value("barcodebuddy", "open_screen_on_start"):
            webbrowser.open_new_tab(f"{self.get_config_value('barcodebuddy', 'bb_server_url')}")
            time.sleep(2)
            webbrowser.open_new_tab(f"{self.get_config_value('barcodebuddy', 'bb_server_url')}screen.php")
            if self.get_config_value("barcodebuddy", "fullscreen_on_start"):
                time.sleep(2)
                os.system("xdotool key F11")
        self._server.start()

    def stop(self, *_):
        self.stop_activity_detection()
        self._scanner.off()
        self._backlight.on()
        GPIO.cleanup()
        sys.exit(0)

    def setup_activity_detection(self):
        if not self.get_config_value("sleep", "sleep_if_no_activity"):
            return None
        if self.get_config_value("sleep", "activity_detection_mode") == "motion":
            ad = activitydetection_motion.ActivityDetectionMotion(self)
        else:
            ad = activitydetection_voice.ActivityDetectionVoice(self)
        ad.start()
        return ad

    def stop_activity_detection(self):
        if not self._activitydetection:
            return
        self._activitydetection.terminate()
        self._activitydetection.join()

    def on_activity_detected(self):
        self._scanner.on()
        self._backlight.on()
        if self.get_config_value("barcodebuddy", "open_screen_on_start") and \
                self.get_config_value("barcodebuddy", "reload_page_after_sleep"):
            os.system("xdotool search --onlyvisible --class Chromium windowfocus key ctrl+r")

    def on_sleep_started(self):
        self._scanner.off()
        self._backlight.off()

    def start_speech_recognition(self):
        self._speechrecognition.start_recording()

    def get_config_value(self, *path):
        value = self.search_config_value(self._config, path)
        if value is None:
            return self.search_config_value(self._config_default, path)
        else:
            return value

    @staticmethod
    def search_config_value(value, path):
        for key in path:
            if key not in value:
                continue
            value = value[key]
            if key == path[-1]:
                return value
