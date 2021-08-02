import threading
import time
from . import tuning
import usb.core
import usb.util


class ActivityDetectionMotion(threading.Thread):

    def __init__(self, pantryscanner):
        super().__init__()
        self._pantryscanner = pantryscanner
        self._timeout_secs: int = self._pantryscanner.get_config_value("sleep", "sleep_after_secs")
        self._terminate = False
        self._new_timer()

    def run(self, *args, **kwargs):
        pass

    def _new_timer(self):
        self._timer = threading.Timer(10, self._pantryscanner.on_sleep_started)
        self._timer.start()

    def terminate(self):
        self._terminate = True
        if self._timer.is_alive():
            self._timer.cancel()
