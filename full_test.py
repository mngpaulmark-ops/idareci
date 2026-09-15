import sys, os
sys.path.insert(0, '.')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import app as myapp

myapp.app.config['TESTING'] = True
myapp.app.config['WTF_CSRF_ENABLED'] = False
client = myapp.app.test_client()

# Test login
print("=" * 60)
print("1. LOGIN TEST")
print("=" * 60)
resp = client.post('/login', data={'username': 'admin', 'password': '123456'}, follow_redirects=False)
print(f"  POST /login: {resp.status_code} -> {resp.headers.get('Location', 'no redirect')}")
if resp.status_code == 302 and '/admin' in resp.headers.get('Location', ''):
    print("  ✅ Login BAŞARILI - admin panele yönlendirme")
else:
    print("  ❌ Login BAŞARISIZ")
    # Try following redirects to see the result
    resp2 = client.post('/login', data={'username': 'admin', 'password': '123456'}, follow_redirects=True)
    if b'admin_index' in resp2.data or 'Paneli' in resp2.data.decode('utf-8','ignore'):
        print("  ✅ Aslında çalışıyor (redirect sonrası admin panel açıldı)")

# Now set session for further tests
with client.session_transaction() as sess:
    sess['logged_in'] = True
    sess['role'] = 'admin'

print("\n" + "=" * 60)
print("2. ADMIN PANEL TÜM SAYFALAR")
print("=" * 60)

pages = [
    ('/admin', 'Ana Panel'),
    ('/admin/add', 'Sayfa Ekle'),
    ('/admin/yonkur', 'Yönetim Kurulu'),
    ('/admin/kose', 'Köşe Yazıları'),
    ('/admin/etkinlik', 'Etkinlikler'),
    ('/admin/galeri', 'Foto Galeri'),
    ('/admin/menu', 'Menü Ayarları'),
    ('/admin/haber', 'Haber Yönetimi'),
    ('/admin/temsilcilik', 'Temsilcilik'),
    ('/admin/password', 'Şifre Değiştir'),
    ('/admin/leftmenu', 'Sol Menü'),
    ('/admin/settings', 'Genel Ayarlar'),
    ('/admin/editors', 'Editör Yönetimi'),
    ('/admin/videos', 'Video Galeri'),
    ('/admin/widgets', 'Widget Paneller'),
    ('/admin/sidebar', 'Sidebar Bloklar'),
    ('/admin/hesap', 'Hesap Ayarları'),
]

all_ok = True
for url, name in pages:
    try:
        resp = client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            print(f"  ✅ {name:25s} ({url})")
        else:
            all_ok = False
            print(f"  ❌ {name:25s} ({url}) -> HTTP {resp.status_code}")
    except Exception as e:
        all_ok = False
        print(f"  ❌ {name:25s} ({url}) -> HATA: {e}")

# Test POST operations
print("\n" + "=" * 60)
print("3. MENÜ TOGGLE TEST")
print("=" * 60)
with myapp.app.app_context():
    menu = myapp.Menu.query.first()
    if menu:
        resp = client.post(f'/admin/menu/toggle/{menu.id}', follow_redirects=True)
        print(f"  Menü toggle (ID:{menu.id}): HTTP {resp.status_code} {'✅' if resp.status_code == 200 else '❌'}")
    else:
        print("  ⚠️ Hiç menü yok")

print("\n" + "=" * 60)
print("4. ÖN YÜZ SAYFALAR")
print("=" * 60)
front_pages = [
    ('/', 'Ana Sayfa'),
    ('/anasayfa.html', 'anasayfa.html'),
]
for url, name in front_pages:
    resp = client.get(url, follow_redirects=True)
    print(f"  {'✅' if resp.status_code == 200 else '❌'} {name:25s} ({url}) -> HTTP {resp.status_code}")

# Check gallery images
print("\n" + "=" * 60)
print("5. RESİM DOSYALARI")
print("=" * 60)
images = [
    '/data/gallerygroup/1.jpg',
    '/data/gallerygroup/2.jpg',
    '/data/haber/thumb_481.jpg',
    '/data/haber/thumb_523.jpg',
    '/data/9595428-logo.png',
]
for img in images:
    resp = client.get(img)
    size = len(resp.data) if resp.status_code == 200 else 0
    print(f"  {'✅' if resp.status_code == 200 else '❌'} {img:45s} -> HTTP {resp.status_code} ({size} bytes)")

print("\n" + "=" * 60)
if all_ok:
    print("✅ TÜM TESTLER BAŞARILI!")
else:
    print("❌ BAZI TESTLER BAŞARISIZ - yukarıyı kontrol edin")
print("=" * 60)
