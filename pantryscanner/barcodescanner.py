import RPi.GPIO as GPIO


class BarcodeScanner:

    def __init__(self, pantryscanner):
        self._pantryscanner = pantryscanner
        self._gpio_pin_relais: int = self._pantryscanner.get_config_value("scanner", "gpio_pin_relais")

    def on(self):
        GPIO.output(self._gpio_pin_relais, GPIO.HIGH)

    def off(self):
        GPIO.output(self._gpio_pin_relais, GPIO.LOW)
