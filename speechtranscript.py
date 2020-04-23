import json
from os import environ
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(environ['IBM_API_KEY'])
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url(environ['IBM_URL'])

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        response_text = json.dumps(data, indent=4)
        response_dict = json.loads(response_text)

        print(response_dict['results'][0]['alternatives'][0]['transcript'])
        return response_dict['results'][0]['alternatives'][0]['transcript']
        # ['alternatives'][0]['transcript'])

        # print(json.dumps(data, indent=4))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

class SpeechTranscript():
    def __init__(self):
        authenticator = IAMAuthenticator(environ['IBM_API_KEY'])
        self.speech_to_text = SpeechToTextV1(
            authenticator=authenticator
        )
        speech_to_text.set_service_url(environ['IBM_URL'])

        self.myRecognizeCallback = MyRecognizeCallback()

    def transcript(self, file_path='./.', file_name='audio-file.flac'):
        with open(join(dirname(__file__), file_path, file_name), 'rb') as audio_file:
            audio_source = AudioSource(audio_file)
            speech_to_text.recognize_using_websocket(
                audio=audio_source,
                content_type='audio/mp3',
                recognize_callback=self.myRecognizeCallback,
                model='ja-JP_BroadbandModel',)
