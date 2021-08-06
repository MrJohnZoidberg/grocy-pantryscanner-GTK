import speech_recognition as sr
import threading
import requests
from pixel_ring import pixel_ring


class SpeechRecognition:
    def __init__(self, pantryscanner):
        self._r = sr.Recognizer()
        self._recording_thread = None
        self._pantryscanner = pantryscanner
        self._bb_api_url = self._pantryscanner.get_config_value('barcodebuddy', 'bb_server_url') + "api/"
        self._bb_api_key = self._pantryscanner.get_config_value('barcodebuddy', 'bb_api_key')
        pixel_ring.off()
        pixel_ring.set_vad_led(0)

    def start_recording(self):
        self._recording_thread = threading.Thread(target=self._record_speech)
        self._recording_thread.start()

    def _record_speech(self):
        # obtain audio from the microphone
        with sr.Microphone() as source:
            print("Say something!")
            pixel_ring.spin()
            audio = self._r.listen(source)
        pixel_ring.off()
        self._result(audio)

    def _result(self, audio):
        # recognize speech using Google Speech Recognition
        try:
            text = self._r.recognize_google(audio, language="de-DE")
            print("Google Speech Recognition hat verstanden: " + text)
            requests.get(self._bb_api_url + 'action/product?apikey=' + self._bb_api_key
                         + '&name=' + text)
        except sr.UnknownValueError:
            print("Google Speech Recognition konnte Audio nicht verstehen")
        except sr.RequestError as e:
            print("Anfrage zu Google Speech Recognition ist fehlgeschlagen; {0}".format(e))
