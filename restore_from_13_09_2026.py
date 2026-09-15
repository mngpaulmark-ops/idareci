import os
import shutil
import sqlite3
import bs4

backup_dir = r"C:\Users\turga\OneDrive\Desktop\temp_backup_13_test"
target_dir = r"C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org"

pages_to_restore = [
    'hakkimizda.html',
    'tuzugumuz.html',
    'yonetimkurulu.html',
    'baskanlik-ve-birimler.html',
    'yuksek-istisare-onur-kurulu-uyesi.html',
    'diger-kurullar.html',
    'temsilcilik.html',
    'uyelik.html',
    'resimler.html',
    'videolar.html'
]

conn = sqlite3.connect(os.path.join(target_dir, 'instance', 'cms.db'))
c = conn.cursor()

for page_file in pages_to_restore:
    src = os.path.join(backup_dir, page_file)
    dst = os.path.join(target_dir, page_file)
    
    if os.path.exists(src):
        # 1. Copy the file directly to restore perfectly
        shutil.copy2(src, dst)
        print(f"Restored {page_file} from 13.09.2026 backup.")
        
        # 2. Extract its content and update the DB so Admin panel has the identical content
        with open(dst, 'r', encoding='utf-8', errors='surrogateescape') as f:
            html = f.read()
            
        soup = bs4.BeautifulSoup(html, 'html.parser')
        main_div = soup.find('div', id='main')
        if main_div:
            # We want the content inside the box or panel-body
            panel_body = main_div.find('div', class_='panel-body')
            if panel_body:
                box = panel_body.find('div', class_='box')
                if box:
                    content = "".join(str(item) for item in box.contents).strip()
                else:
                    content = "".join(str(item) for item in panel_body.contents).strip()
                    
                slug = page_file.replace('.html', '')
                c.execute('UPDATE page SET content_html=? WHERE slug=?', (content, slug))

conn.commit()
conn.close()
print("All pages restored from 13.09.2026 and DB synced!")
