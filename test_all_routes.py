import sys
sys.path.insert(0, '.')
import app as myapp

myapp.app.config['TESTING'] = True
client = myapp.app.test_client()

with client.session_transaction() as sess:
    sess['logged_in'] = True
    sess['user_id'] = 1
    sess['role'] = 'admin'

routes_to_test = [
    ('GET', '/admin'),
    ('GET', '/admin/add'),
    ('GET', '/admin/yonkur'),
    ('GET', '/admin/kose'),
    ('GET', '/admin/etkinlik'),
    ('GET', '/admin/galeri'),
    ('GET', '/admin/menu'),
    ('GET', '/admin/haber'),
    ('GET', '/admin/temsilcilik'),
    ('GET', '/admin/password'),
    ('GET', '/admin/leftmenu'),
    ('GET', '/admin/settings'),
    ('GET', '/admin/editors'),
    ('GET', '/admin/videos'),
    ('GET', '/admin/widgets'),
    ('GET', '/admin/sidebar'),
    ('GET', '/admin/hesap'),
]

print("=" * 60)
print("ADMIN PANEL ROUTE TEST RESULTS")
print("=" * 60)

all_pass = True
for method, path in routes_to_test:
    try:
        if method == 'GET':
            resp = client.get(path, follow_redirects=True)
        else:
            resp = client.post(path, follow_redirects=True)
        
        status = 'OK' if resp.status_code == 200 else f'FAIL ({resp.status_code})'
        if resp.status_code != 200:
            all_pass = False
            # Try to get error info
            data = resp.data.decode('utf-8', errors='ignore')[:200]
            print(f"  {method} {path}: {status}")
            print(f"    Response: {data}")
        else:
            print(f"  {method} {path}: {status}")
    except Exception as e:
        all_pass = False
        print(f"  {method} {path}: EXCEPTION - {e}")

print("=" * 60)
if all_pass:
    print("ALL ROUTES PASSED!")
else:
    print("SOME ROUTES FAILED - see above")
print("=" * 60)
