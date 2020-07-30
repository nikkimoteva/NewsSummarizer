from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class ToneAnalyzer:
    key= "jxx8RieqMFdSJXuOuU8nitYOWEEzUMAehR675dX7jEFk"
    url= "https://api.au-syd.tone-analyzer.watson.cloud.ibm.com/instances/420d78a0-a1ed-4280-b409-8cd943ef5746"
    authenticator = IAMAuthenticator(key)
    tone_analyzer = ToneAnalyzerV3(authenticator=authenticator, version='4.5.0')

    tone_analyzer.set_service_url(url)