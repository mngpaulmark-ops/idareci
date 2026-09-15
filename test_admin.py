import urllib.request
import app
app.app.config['TESTING'] = True
client = app.app.test_client()

with client.session_transaction() as sess:
    sess['user_id'] = 1
    sess['role'] = 'admin'

resp = client.get('/admin', follow_redirects=True)
print(f"Status code: {resp.status_code}")
if resp.status_code != 200:
    print(resp.data.decode('utf-8'))
