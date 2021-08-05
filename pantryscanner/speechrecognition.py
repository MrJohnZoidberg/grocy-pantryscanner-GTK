import speech_recognition as sr
import threading


class SpeechRecognition:
    def __init__(self, pantryscanner):
        self._r = sr.Recognizer()
        self._recording_thread = None
        self._pantryscanner = pantryscanner

    def start_recording(self):
        self._recording_thread = threading.Thread(target=self._record_speech)
        self._recording_thread.start()

    def _record_speech(self):
        # obtain audio from the microphone
        with sr.Microphone() as source:
            print("Say something!")
            audio = self._r.listen(source)
        self._result(audio)

    def _result(self, audio):
        # recognize speech using Google Speech Recognition
        try:
            print("Google Speech Recognition thinks you said " + self._r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
