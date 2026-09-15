import sqlite3
import bs4
import re
import os

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()

c.execute('SELECT id, slug, title FROM page')
pages = c.fetchall()

for p_id, slug, title in pages:
    filename = f"{slug}.html"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8', errors='surrogateescape') as f:
            html = f.read()
            
        soup = bs4.BeautifulSoup(html, 'html.parser')
        
        main_div = soup.find('div', id='main')
        if main_div:
            panel_body = main_div.find('div', class_='panel-body')
            if panel_body:
                # Extract inner content
                box = panel_body.find('div', class_='box')
                if box:
                    content = "".join(str(item) for item in box.contents).strip()
                else:
                    content = "".join(str(item) for item in panel_body.contents).strip()
                
                c.execute('UPDATE page SET content_html=? WHERE id=?', (content, p_id))
                print(f"Updated '{slug}' from LOCAL file!")
            else:
                print(f"Panel body not found for '{slug}'")
        else:
            print(f"Main div not found for '{slug}'")

# Now update the menus properly
c.execute("DELETE FROM menu")
c.execute("DELETE FROM left_menu")

menus = [
    ('Ana Sayfa', 'anasayfa.html', 1),
    ('Derneğimiz', '#', 2),
    ('Haberler', 'haber-listesi.html', 3),
    ('Etkinlikler', 'etkinlik.html', 4),
    ('Fotoğraf Galerisi', 'resimler.html', 5),
    ('Video Galerisi', 'videolar.html', 6),
    ('İletişim', 'iletisim.html', 7)
]
for title, url, order in menus:
    c.execute("INSERT INTO menu (title, url, \"order\") VALUES (?, ?, ?)", (title, url, order))

# We can also add some drop downs for Derneğimiz (parent_id = 2)
c.execute("SELECT id FROM menu WHERE title='Derneğimiz'")
dernegimiz_id = c.fetchone()[0]

sub_menus = [
    ('Hakkımızda', 'hakkimizda.html', 1),
    ('Tüzüğümüz', 'tuzugumuz.html', 2),
    ('Yönetim Kurulu', 'yonetimkurulu.html', 3),
    ('Başkanlık ve Birimler', 'baskanlik-ve-birimler.html', 4),
    ('Yüksek İstişare ve Onur Kurulu', 'yuksek-istisare-onur-kurulu-uyesi.html', 5),
    ('Diğer Kurullar', 'diger-kurullar.html', 6),
    ('Temsilcilik', 'temsilcilik.html', 7),
    ('Üyelerimiz', 'uyelik.html', 8),
]
for title, url, order in sub_menus:
    c.execute("INSERT INTO menu (title, url, \"order\", parent_id) VALUES (?, ?, ?, ?)", (title, url, order, dernegimiz_id))

left_menus = [
    (' Hakkımızda', 'hakkimizda.html', 1),
    (' Yönetim Kurulu', 'yonetimkurulu.html', 2),
    (' Başkanlık ve Birimler', 'baskanlik-ve-birimler.html', 3),
    (' Projeler', '#', 4),
    (' Yüksek İstişare ve Onur Kurulu', 'yuksek-istisare-onur-kurulu-uyesi.html', 5),
    (' Diğer Kurullar', 'diger-kurullar.html', 6),
    (' Temsilcilikler', 'temsilcilik.html', 7),
    (' Gençlik Kolları', 'genclik-kollari.html', 8),
    (' Üyelerimiz', 'uyelik.html', 9),
    (' Haberler', 'haber-listesi.html', 10),
    (' Duyurular', 'duyurular.html', 11),
    (' Etkinlikler', 'etkinlik.html', 12),
    (' Raporlar / Belgeler', 'raporlar-belgeler.html', 13)
]
for title, url, order in left_menus:
    c.execute("INSERT INTO left_menu (title, url, \"order\") VALUES (?, ?, ?)", (title, url, order))

conn.commit()
conn.close()
print("All pages and menus populated correctly into CMS DB!")
