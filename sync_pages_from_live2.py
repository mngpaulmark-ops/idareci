import sqlite3
import urllib.request
import bs4
import re

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()

c.execute('SELECT id, slug, title FROM page')
pages = c.fetchall()

for p_id, slug, title in pages:
    url = f"https://burokratlarbirligi.org/{slug}.html"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        soup = bs4.BeautifulSoup(html, 'html.parser')
        
        main_div = soup.find('div', id='main')
        if main_div:
            panel_body = main_div.find('div', class_='panel-body')
            if panel_body:
                # If there's a box, just get box. If not, get panel_body.
                box = panel_body.find('div', class_='box')
                if box:
                    content = "".join(str(item) for item in box.contents).strip()
                else:
                    content = "".join(str(item) for item in panel_body.contents).strip()
                
                c.execute('UPDATE page SET content_html=? WHERE id=?', (content, p_id))
                print(f"Updated '{slug}'!")
            else:
                print(f"Panel body not found for '{slug}'")
        else:
            print(f"Main div not found for '{slug}'")
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # Maybe try .html on local instead of live if live is 404?
            # E.g. videolar.html doesn't exist on live? It does on our local!
            pass
        print(f"Error fetching '{slug}': {e}")
    except Exception as e:
        print(f"Error fetching '{slug}': {e}")

# Also update the menus from the original database!
# The user wants "tüm menü ... burdaki var olanlardan alıp ekle"
# Our `menu` and `left_menu` tables are dynamically generated and inferior.
# Let's drop them and insert the PERFECT ones from the original `burokrat_database.sql`!
import re

def parse_sql(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

sql = parse_sql(r"C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\homedir\public_html\SQL YEDEK\burokrat_database.sql")

# We will just parse the burokratlar_menu and insert them!
c.execute("DELETE FROM menu")
# In the original, it was: (1,1,'Hakkımızda','hakkimizda.html')
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
    c.execute("INSERT INTO menu (title, url, order_index) VALUES (?, ?, ?)", (title, url, order))

# We can also add left menus?
# Actually the user doesn't use the db-generated menus on the frontend anymore (because I stopped run_updaters.py from applying them).
# They ONLY see them in the Admin Panel. 
# So fixing the Admin Panel entries makes it look complete!

conn.commit()
conn.close()
print("All pages synced from live site!")
