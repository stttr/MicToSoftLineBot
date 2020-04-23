import json
from os import environ
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class SpeechTranscript():
    def __init__(self):
        authenticator = IAMAuthenticator(environ['IBM_API_KEY'])
        self.speech_to_text = SpeechToTextV1(
            authenticator=authenticator
        )
        self.speech_to_text.set_service_url(environ['IBM_URL'])

    def transcript(self, file_path='./', file_name='audio-file.flac'):
        with open(join(dirname(__file__), file_path, file_name), 'rb') as audio_file:
            response = self.speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/mp3',
            model='ja-JP_BroadbandModel',)

            response_dic = response.get_result()
            print(response_dic['results'][0]['alternatives'][0]['transcript'])
            return response_dic['results'][0]['alternatives'][0]['transcript']
