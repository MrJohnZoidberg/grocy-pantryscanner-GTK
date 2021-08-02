from . import mainwindow
from . import grocy
from . import displaybacklight
from . import activitydetection_voice
from . import activitydetection_motion
from . import barcodescanner
import gi
import RPi.GPIO as GPIO
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PantryScanner:

    def __init__(self, config, config_default):
        GPIO.setmode(GPIO.BCM)
        self._config = config
        self._config_default = config_default
        self._grocy = grocy.Grocy(self)
        self._backlight = displaybacklight.DisplayBacklight()
        self._activitydetection = self.setup_activity_detection()
        self._scanner = barcodescanner.BarcodeScanner(self)

    def start(self):
        mainwindow.MainWindow(self)
        Gtk.main()

    def stop(self, *_):
        self.stop_activity_detection()
        self._backlight.on()
        Gtk.main_quit()

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
        self._backlight.on()
        self._scanner.on()

    def on_sleep_started(self):
        self._backlight.off()
        self._scanner.off()

    def get_config_value(self, *path):
        value = self.search_config_value(self._config, path)
        if value is None:
            return self.search_config_value(self._config_default, path)

    @staticmethod
    def search_config_value(value, path):
        for key in path:
            if key not in value:
                continue
            value = value[key]
            if key == path[-1]:
                return value
