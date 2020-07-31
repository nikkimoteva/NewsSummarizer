from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def ToneAnalyzer(text):
    apiKey= "jxx8RieqMFdSJXuOuU8nitYOWEEzUMAehR675dX7jEFk"
    url= "https://api.au-syd.tone-analyzer.watson.cloud.ibm.com/instances/420d78a0-a1ed-4280-b409-8cd943ef5746"
    authenticator = IAMAuthenticator(apiKey)

    authenticator = IAMAuthenticator(apiKey)
    toneAnalyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )

    toneAnalyzer.set_service_url(url)

    tone = toneAnalyzer.tone(
        {'text': text},
        content_type='application/json'
    ).get_result()
    if tone:
        if tone['document_tone']:
            if tone["document_tone"]['tones']:
                if tone["document_tone"]['tones'][0]:
                    if tone["document_tone"]['tones'][0]['score']:
                        return tone["document_tone"]['tones'][0]['score']
    return -1