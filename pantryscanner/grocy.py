class Grocy:

    def __init__(self, pantryscanner):
        self._server_url = pantryscanner.get_config_value("grocy", "server_url")
        if self._server_url[-1] == "/":
            self._api_url = self._server_url + "api"
        else:
            self._api_url = self._server_url + "/api"
