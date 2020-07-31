import requests, uuid, json

def Translate(langFrom, langTo, text):
    apiKey = '85c15359e016483483c6d4501ecea3ed'
    endpoint = 'https://api.cognitive.microsofttranslator.com/'

    path = '/translate?api-version=3.0'
    params = "&from=" + langFrom +"&to=" + langTo
    constructedUrl = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': apiKey,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    if len(text) > 5000:
        text = text[:5000]

    body = [{
        'text' : text

    }]
    request = requests.post(constructedUrl, headers=headers, json=body)
    if request.json():
        if request.json()[0]:
            response = request.json()[0]["translations"]
            return response[0]['text']
    else: return "dang"