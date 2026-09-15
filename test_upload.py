import requests
import os

url = 'http://127.0.0.1:5005/login'
session = requests.Session()
res = session.post(url, data={'username': 'admin', 'password': '123456'})

if res.status_code == 200 and 'Admin Paneli' in res.text:
    print("Logged in!")
else:
    print("Login failed")

# Create dummy image
with open('test_img.jpg', 'wb') as f:
    f.write(os.urandom(1024))

url_edit = 'http://127.0.0.1:5005/admin/temsilcilik/edit/1'
files = {'image': ('test_img.jpg', open('test_img.jpg', 'rb'), 'image/jpeg')}
data = {
    'city_code': 'TR-34',
    'name': 'Test Rep',
    'phone': '123456'
}

res2 = session.post(url_edit, data=data, files=files)
print("Edit status:", res2.status_code)
if 'Internal Server Error' in res2.text:
    print("Internal Server Error occurred!")
elif 'Temsilcilik gǬncellendi' in res2.text or 'Temsilcilik g' in res2.text or res2.status_code == 200:
    print("Update successful!")
else:
    print("Update failed?", res2.text[:200])
