import threading
import time
from . import tuning
import usb.core
import usb.util


class VAD(threading.Thread):

    def __init__(self, pantryscanner):
        super().__init__()
        self._pantryscanner = pantryscanner
        self._terminate = False
        self._dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

    def run(self, *args, **kwargs):
        if self._dev:
            tun = tuning.Tuning(self._dev)
            while not self._terminate:
                try:
                    if tun.is_voice():
                        self._pantryscanner.screen_dimmed()
                        time.sleep(5)
                        self._pantryscanner.screen_bright()
                    time.sleep(0.05)
                except KeyboardInterrupt:
                    break
        else:
            while not self._terminate:
                time.sleep(0.5)

    def terminate(self):
        self._terminate = True
