from flask import Flask, json
import threading

api = Flask(__name__)


class Server:
    def __init__(self, pantryscanner):
        self._server_thread = None
        global _pantryscanner
        _pantryscanner = pantryscanner

    def start(self):
        self._server_thread = threading.Thread(target=api.run, args=("localhost", "1234"))
        self._server_thread.start()

    @staticmethod
    @api.route('/toggle_listening', methods=['POST'])
    def start_listening():
        _pantryscanner.start_speech_recognition()
        return json.dumps({"success": True}), 201


if __name__ == "__main__":
    server = Server(None)
    server.start()
