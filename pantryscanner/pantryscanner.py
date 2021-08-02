from . import mainwindow
from . import grocy
from . import vad
from rpi_backlight import Backlight
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PantryScanner:

    def __init__(self, config, config_default):
        self._config = config
        self._config_default = config_default
        self._grocy = grocy.Grocy(self)
        self._vad = vad.VAD(self)
        self._vad.start()
        self._backlight = Backlight()
        self._backlight.power = True
        self._backlight.fade_duration = 0.5

    def start(self):
        mainwindow.MainWindow(self)
        Gtk.main()

    def stop(self, *_):
        self._vad.terminate()
        self._vad.join()
        Gtk.main_quit()

    def on_activity_detected(self):
        self._backlight.power = True
        self._backlight.brightness = 100

    def on_sleep_started(self):
        self._backlight.brightness = 0

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
