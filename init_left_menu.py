import sqlite3

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS left_menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    url VARCHAR(255) NOT NULL,
    "order" INTEGER,
    is_active BOOLEAN
)''')

items = [
    ('Hakkımızda', 'hakkimizda.html'),
    ('Yönetim Kurulu', 'yonetimkurulu.html'),
    ('Başkanlık ve Birimler', 'baskanlik-ve-birimler.html'),
    ('Projeler', '#'),
    ('Yüksek İstişare ve Onur Kurulu', 'yuksek-istisare-onur-kurulu-uyesi.html'),
    ('Diğer Kurullar', 'diger-kurullar.html'),
    ('Temsilcilikler', 'temsilcilik.html'),
    ('Gençlik Kolları', './?mod=page&id=5'),
    ('Üyelerimiz', '#'),
    ('Haberler', 'haberler.html'),
    ('Duyurular', '#'),
    ('Etkinlikler', 'etkinlik.html'),
    ('Raporlar / Belgeler', '#')
]

c.execute('SELECT COUNT(*) FROM left_menu')
if c.fetchone()[0] == 0:
    for i, (title, url) in enumerate(items):
        c.execute('INSERT INTO left_menu (title, url, "order", is_active) VALUES (?, ?, ?, 1)', (title, url, i))
conn.commit()
conn.close()
print('Initialized left_menu table')
