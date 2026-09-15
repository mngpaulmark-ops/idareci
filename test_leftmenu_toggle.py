import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import app
app.app.config['TESTING'] = True
client = app.app.test_client()

with client.session_transaction() as sess:
    sess['user_id'] = 1
    sess['role'] = 'admin'

resp = client.post('/admin/leftmenu/toggle/1', follow_redirects=True)
print(f"Status code: {resp.status_code}")
if resp.status_code != 200:
    print(resp.data.decode('utf-8'))
