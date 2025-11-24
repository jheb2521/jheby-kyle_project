import json
import urllib.request

URL = 'http://127.0.0.1:5000/api/chat'

def post(message, extra=None):
    payload = {'message': message}
    if extra:
        payload.update(extra)
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            print('Request:', payload)
            print('Response:', resp.read().decode('utf-8'))
    except Exception as e:
        print('Request failed:', payload, 'Error:', e)

if __name__ == '__main__':
    post('hi')
    post('laptop')
    post('Tell me about MacBook Air')
