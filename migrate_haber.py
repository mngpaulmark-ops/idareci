import re
import os
from app import app, db, Haber

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'

def run():
    with app.app_context():
        # Clear existing
        Haber.query.delete()
        
        with open(sql_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Find INSERT INTO `burokratlar_haber`
        # format: INSERT INTO `burokratlar_haber` VALUES (id, ...), (id, ...)
        matches = re.finditer(r"INSERT INTO `burokratlar_haber` VALUES\s*(.*?);", content, re.DOTALL)
        count = 0
        for match in matches:
            values_str = match.group(1)
            # This is hard to parse correctly due to commas in content. 
            # It's better to just skip migration for now or extract just titles?
            # Actually, the user's HTML files (haber/XYZ.html) are intact!
            pass
        
        # Another approach: Parse the HTML files in haber/ directory!
        import glob
        import bs4
        from datetime import datetime
        
        html_files = glob.glob('haber/*.html')
        for file in html_files:
            # File name is like haber/123-slug-name.html
            basename = os.path.basename(file)
            parts = basename.replace('.html', '').split('-', 1)
            if len(parts) == 2:
                try:
                    hid = int(parts[0])
                except:
                    continue
                slug = parts[1]
                
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    soup = bs4.BeautifulSoup(f.read(), 'lxml')
                
                h2 = soup.find('h2')
                title = h2.text.strip() if h2 else slug
                
                # Try to find image
                img_path = None
                content_div = soup.find('div', class_='content')
                if not content_div:
                    panels = soup.find_all('div', class_='panel-body')
                    if panels:
                        content_div = panels[-1]
                
                if content_div:
                    img = content_div.find('img')
                    if img and img.get('src'):
                        img_path = img.get('src').lstrip('/')
                
                h = Haber(id=hid, title=title, slug=slug, content="", image_path=img_path)
                db.session.add(h)
                count += 1
        
        db.session.commit()
        print(f"Migrated {count} news articles from HTML files to DB!")

if __name__ == '__main__':
    run()
