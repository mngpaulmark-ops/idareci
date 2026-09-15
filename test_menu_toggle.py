import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

# We need to simulate a login and then a POST to /admin/menu/toggle/1
# To do this, we'll write a quick Flask test_client script
import app
app.app.config['TESTING'] = True
client = app.app.test_client()

# 1. Login
with client.session_transaction() as sess:
    sess['user_id'] = 1
    sess['role'] = 'admin'

# 2. POST to toggle
resp = client.post('/admin/menu/toggle/1', follow_redirects=True)
print(f"Status code: {resp.status_code}")
if resp.status_code != 200:
    print(resp.data.decode('utf-8'))
