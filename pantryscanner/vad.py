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
        self._timer = None

    def run(self, *args, **kwargs):
        if self._dev:
            while not self._terminate:
                if self._tun.is_voice():
                    print("New timer started")
                    if self._timer and self._timer.is_alive():
                        self._timer.cancel()
                    else:
                        self.on_voice_detected()

                    self._timer = threading.Timer(10, self.on_timer_finished)
                    self._timer.start()
                    threading.Timer(2, self.run).start()
                    return
                else:
                    time.sleep(0.05)
        else:
            while not self._terminate:
                time.sleep(0.5)

    def on_voice_detected(self):
        self._pantryscanner.screen_dimmed()

    def on_timer_finished(self):
        self._pantryscanner.screen_bright()

    def terminate(self):
        self._terminate = True
        if self._timer.is_alive():
            self._timer.cancel()
