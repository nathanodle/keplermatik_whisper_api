import requests

url = 'http://192.168.1.2:8002/upload'
file = {'file': open('test.wav', 'rb')}
resp = requests.post(url=url, files=file)
print(resp.json()["transcription_result"]["text"])