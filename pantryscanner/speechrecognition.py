import speech_recognition as sr
import threading
import requests
import pyglet
from pixel_ring import pixel_ring


class SpeechRecognition:
    def __init__(self, pantryscanner):
        self._pantryscanner = pantryscanner
        self._bb_api_url = self._pantryscanner.get_config_value('barcodebuddy', 'bb_server_url') + "api/"
        self._bb_api_key = self._pantryscanner.get_config_value('barcodebuddy', 'bb_api_key')
        pixel_ring.off()
        pixel_ring.set_vad_led(0)
        self._start_sound = pyglet.media.load("resources/start_listening.wav", streaming=False)
        self._stop_sound = pyglet.media.load("resources/stop_listening.wav", streaming=False)
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        self.is_listening = False
        self._stop_listening_method = None
        with self._microphone as source:
            self._start_sound.play()
            pixel_ring.spin()
            # we only need to calibrate once, before we start listening
            self._recognizer.adjust_for_ambient_noise(source)
            self._stop_sound.play()
            pixel_ring.off()

    def start_listening(self):
        self.is_listening = True
        self._start_sound.play()
        pixel_ring.spin()
        self._stop_listening_method = self._recognizer.listen_in_background(self._microphone, self._callback)

    def stop_listening(self):
        self._stop_listening_method(True)
        pixel_ring.off()
        self._stop_sound.play()
        self.is_listening = False

    def _callback(self, recognizer, audio):
        self.stop_listening()
        # recognize speech using Google Speech Recognition
        try:
            text = recognizer.recognize_google(audio, language="de-DE")
            print("Google Speech Recognition hat verstanden: " + text)
            requests.get(self._bb_api_url + 'action/product?apikey=' + self._bb_api_key
                         + '&name=' + text)
        except sr.UnknownValueError:
            print("Google Speech Recognition konnte Audio nicht verstehen")
        except sr.RequestError as e:
            print("Anfrage zu Google Speech Recognition ist fehlgeschlagen; {0}".format(e))
