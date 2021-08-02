import threading
import time
from . import tuning
import usb.core
import usb.util


class VAD(threading.Thread):

    def __init__(self, pantryscanner):
        super().__init__()
        self._pantryscanner = pantryscanner
        self._dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
        self._tun = tuning.Tuning(self._dev)
        self._terminate = False
        self._new_timer()

    def run(self, *args, **kwargs):
        if self._dev:
            while not self._terminate:
                if self._tun.is_voice():
                    print("New timer started")
                    if self._timer and self._timer.is_alive():
                        self._timer.cancel()
                    else:
                        self._pantryscanner.on_activity_detected()

                    self._new_timer()
                    threading.Timer(2, self.run).start()
                    return
                else:
                    time.sleep(0.05)
        else:
            while not self._terminate:
                time.sleep(0.5)

    def _new_timer(self):
        self._timer = threading.Timer(10, self._pantryscanner.on_sleep_started)
        self._timer.start()

    def terminate(self):
        self._terminate = True
        if self._timer.is_alive():
            self._timer.cancel()
