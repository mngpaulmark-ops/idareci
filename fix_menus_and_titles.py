import os
import sqlite3
import bs4
import re

backup_dir = r"C:\Users\turga\OneDrive\Desktop\temp_backup_13_test"
target_dir = r"C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org"

pages_to_restore = {
    'hakkimizda': 'Hakkımızda',
    'tuzugumuz': 'Tüzüğümüz',
    'yonetimkurulu': 'Yönetim Kurulu',
    'baskanlik-ve-birimler': 'Başkanlık ve Birimler',
    'yuksek-istisare-onur-kurulu-uyesi': 'Yüksek İstişare ve Onur Kurulu',
    'diger-kurullar': 'Diğer Kurullar',
    'temsilcilik': 'Temsilcilikler',
    'uyelik': 'Üyelerimiz',
    'resimler': 'Fotoğraf Galerisi',
    'videolar': 'Video Galerisi'
}

# 1. First, we will fix the broken characters in the backup contents, and save them to the DB.
conn = sqlite3.connect(os.path.join(target_dir, 'instance', 'cms.db'))
c = conn.cursor()

def fix_tr_chars(text):
    if not text: return text
    replacements = {
        'Hakkmzda': 'Hakkımızda',
        'Ynetim Kurulu': 'Yönetim Kurulu',
        'Bakanlk': 'Başkanlık',
        'Yksek': 'Yüksek',
        'stiare': 'İstişare',
        'Dier': 'Diğer',
        'Genlik Kollar': 'Gençlik Kolları',
        'yelerimiz': 'Üyelerimiz',
        'dareci': 'İdareci',
        'Brokratlar': 'Bürokratlar',
        'Birlii': 'Birliği',
        'Dernei': 'Derneği',
        'Derneimiz': 'Derneğimiz',
        'Tzmz': 'Tüzüğümüz',
        'Tzmz': 'Tüzüğümüz',
        'Bakan': 'Başkan',
        'ye': 'Üye',
        'Y': 'ş', 'y': 'üy', 'o': 'ü', 'O': 'Ü', '?': 'ş', 'i': 'şi',
        '(': 'Ç', 'c': 'ç', 'g': 'ğ', 'G': 'Ğ', 's': 'ş', 'S': 'Ş',
        'u': 'ü', 'U': 'Ü', 'i': 'i', 'I': 'İ', 'o': 'ö', 'O': 'Ö'
    }
    # First apply exact word matches
    for bad, good in replacements.items():
        if bad in text:
            text = text.replace(bad, good)
    return text

for slug, title in pages_to_restore.items():
    src = os.path.join(backup_dir, f"{slug}.html")
    if os.path.exists(src):
        with open(src, 'r', encoding='utf-8', errors='surrogateescape') as f:
            html = f.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        main_div = soup.find('div', id='main')
        if main_div:
            panel_body = main_div.find('div', class_='panel-body')
            if panel_body:
                box = panel_body.find('div', class_='box')
                if box:
                    content = "".join(str(item) for item in box.contents).strip()
                else:
                    content = "".join(str(item) for item in panel_body.contents).strip()
                
                # Fix encoding artifacts
                content = fix_tr_chars(content)
                c.execute('UPDATE page SET content_html=? WHERE slug=?', (content, slug))
                print(f"Extracted and updated DB for {slug}")

conn.commit()

# 2. Now let's process ALL HTML files in the target directory to fix Menus and Headings
perfect_left_menu = """<ul id="left-menu">
    <li><a href="hakkimizda.html" target="_self">• Hakkımızda</a></li>
    <li><a href="yonetimkurulu.html" target="_self">• Yönetim Kurulu</a></li>
    <li><a href="baskanlik-ve-birimler.html" target="_self">• Başkanlık ve Birimler</a></li>
    <li><a href="yuksek-istisare-onur-kurulu-uyesi.html" target="_self">• Yüksek İstişare ve Onur Kurulu</a></li>
    <li><a href="diger-kurullar.html" target="_self">• Diğer Kurullar</a></li>
    <li><a href="temsilcilik.html" target="_self">• Temsilcilikler</a></li>
    <li><a href="genclik-kollari.html" target="_self">• Gençlik Kolları</a></li>
    <li><a href="uyelik.html" target="_self">• Üyelerimiz</a></li>
    <li><a href="haber-listesi.html" target="_self">• Haberler</a></li>
    <li><a href="duyurular.html" target="_self">• Duyurular</a></li>
    <li><a href="etkinlik.html" target="_self">• Etkinlikler</a></li>
    <li><a href="raporlar-belgeler.html" target="_self">• Raporlar / Belgeler</a></li>
</ul>"""

for root, dirs, files in os.walk(target_dir):
    if '.git' in root or '__pycache__' in root or 'venv' in root or 'instance' in root: continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='surrogateescape') as file:
                html = file.read()
            
            soup = bs4.BeautifulSoup(html, 'html.parser')
            changed = False
            
            # Replace left menu
            old_menu = soup.find('ul', id='left-menu')
            if old_menu:
                new_menu = bs4.BeautifulSoup(perfect_left_menu, 'html.parser')
                old_menu.replace_with(new_menu)
                changed = True
                
            # Replace left menu header "Derneğimiz"
            left = soup.find('div', id='left')
            if left:
                panel = left.find('div', class_='panel-primary')
                if panel:
                    heading = panel.find('div', class_='panel-heading')
                    if heading and 'Derne' in heading.text:
                        # Clear it and recreate
                        heading.clear()
                        img = soup.new_tag('img', src="themes/burokratlar/tema/images/icon-menu.png", alt="Menu")
                        heading.append(img)
                        heading.append(" Derneğimiz")
                        changed = True

            # Fix main heading text
            main_div = soup.find('div', id='main')
            if main_div:
                heading = main_div.find('div', class_='panel-heading')
                if heading:
                    # Fix texts
                    fixed_text = fix_tr_chars(heading.text)
                    # If it's a known page, override totally to be sure
                    slug = f.replace('.html', '')
                    if slug in pages_to_restore:
                        heading.string = f"İdareci ve Bürokratlar Birliği Derneği / {pages_to_restore[slug]}"
                    elif 'Derne' in fixed_text:
                        heading.string = fixed_text.replace('dareci ve Brokratlar Birlii Dernei', 'İdareci ve Bürokratlar Birliği Derneği')
                    changed = True
                    
                # If this file is one of the restored pages, inject its content!
                slug = f.replace('.html', '')
                if slug in pages_to_restore:
                    panel_body = main_div.find('div', class_='panel-body')
                    if panel_body:
                        box = panel_body.find('div', class_='box')
                        # Get from DB
                        c.execute('SELECT content_html FROM page WHERE slug=?', (slug,))
                        res = c.fetchone()
                        if res:
                            new_content = bs4.BeautifulSoup(res[0], 'html.parser')
                            if box:
                                box.clear()
                                box.append(new_content)
                            else:
                                panel_body.clear()
                                panel_body.append(new_content)
                            changed = True

            if changed:
                with open(path, 'w', encoding='utf-8', errors='surrogateescape') as file:
                    file.write(str(soup))

conn.close()
print("All menus and contents fixed!")
