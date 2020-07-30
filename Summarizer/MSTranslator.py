import requests, uuid, json

def translate(lang_from, lang_to, text):
    key = '85c15359e016483483c6d4501ecea3ed'
    endpoint = 'https://api.cognitive.microsofttranslator.com/'

    path = '/translate?api-version=3.0'
    params = "&from=" + lang_from +"&to=" + lang_to
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text' : text

    }]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()[0]
    if response:
        response = request.json()[0]["translations"]
        return response[0]['text']
    else: return "dang"