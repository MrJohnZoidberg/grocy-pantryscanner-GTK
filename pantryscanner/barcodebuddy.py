import threading
import requests


class BarcodeBuddy:

    def __init__(self, pantryscanner):
        self._pantryscanner = pantryscanner
        self._bb_api_url = self._pantryscanner.get_config_value('barcodebuddy', 'bb_server_url') + "api/"
        self._bb_api_key = self._pantryscanner.get_config_value('barcodebuddy', 'bb_api_key')
        self._revert_timer = None
        self.is_state_purchase = False

    def start_revert_timer(self):
        self.stop_revert_timer()
        if not self.is_state_purchase:
            return
        self._revert_timer = threading.Timer(30, self._revert_state_to_consume)

    def stop_revert_timer(self):
        if self._revert_timer and self._revert_timer.is_alive():
            self._revert_timer.cancel()

    def _revert_state_to_consume(self):
        response = requests.post(self._bb_api_url + 'state/setmode?apikey=' + self._bb_api_key, data={'state': 0})
        if response.status_code == 200:
            self.is_state_purchase = False
