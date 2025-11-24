import json
import server

client = server.app.test_client()

def post(message, extra=None):
    payload = {'message': message}
    if extra:
        payload.update(extra)
    resp = client.post('/api/chat', data=json.dumps(payload), content_type='application/json')
    print('Request:', payload)
    print('Status:', resp.status_code)
    try:
        print('Response:', resp.get_json())
    except Exception:
        print('Raw:', resp.data.decode())

if __name__ == '__main__':
    post('hi')
    post('laptop')
    post('Tell me about MacBook Air')
