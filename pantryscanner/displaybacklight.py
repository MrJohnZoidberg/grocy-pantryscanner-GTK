from rpi_backlight import Backlight


class DisplayBacklight:

    def __init__(self):
        self._backlight = Backlight()
        self._backlight.fade_duration = 0.5
        self.on()

    def on(self):
        self._backlight.power = True
        self._backlight.brightness = 100

    def off(self):
        self._backlight.brightness = 0
