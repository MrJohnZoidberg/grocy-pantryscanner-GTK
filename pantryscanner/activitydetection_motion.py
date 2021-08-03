import threading
import time
import RPi.GPIO as GPIO


class ActivityDetectionMotion(threading.Thread):

    def __init__(self, pantryscanner):
        super().__init__()
        self._pantryscanner = pantryscanner
        self._timeout_secs: int = self._pantryscanner.get_config_value("sleep", "sleep_after_secs")
        self._gpio_pir: int = self._pantryscanner.get_config_value("sleep", "motion_detection", "gpio_pir")
        self._pause_timer = None
        self._detection_active = True
        self._terminate = False
        self._new_timer()

    def run(self, *args, **kwargs):
        while not self._terminate:
            if GPIO.input(self._gpio_pir) and self._detection_active:
                if self._timer and self._timer.is_alive():
                    self._timer.cancel()
                else:
                    self._pantryscanner.on_activity_detected()

                self._new_timer()
                self._pause_for_few_secs()
            else:
                time.sleep(0.2)

    def _pause_for_few_secs(self):
        if self._pause_timer and self._pause_timer.is_alive():
            self._pause_timer.cancel()
        self._detection_active = False
        self._pause_timer = threading.Timer(3, self._activate_detection)
        self._pause_timer.start()

    def _activate_detection(self):
        self._detection_active = True

    def _new_timer(self):
        self._timer = threading.Timer(self._timeout_secs, self._start_sleep_and_pause)
        self._timer.start()

    def _start_sleep_and_pause(self):
        self._pantryscanner.on_sleep_started()
        self._pause_for_few_secs()

    def terminate(self):
        self._terminate = True
        if self._pause_timer and self._pause_timer.is_alive():
            self._pause_timer.cancel()
        if self._timer and self._timer.is_alive():
            self._timer.cancel()
