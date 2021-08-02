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

    def start(self):
        self.screen_bright()
        win = mainwindow.MainWindow(self)
        Gtk.main()

    def stop(self, *_):
        self._vad.terminate()
        self._vad.join()
        Gtk.main_quit()

    def screen_bright(self):
        self._backlight.brightness = 100

    def screen_dimmed(self):
        self._backlight.brightness = 20

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
