import re

with open('update_anasayfa.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("from app import app, db, Haber", "from app import app, db, Haber, Duyuru")

injection = """
        # DUYURULAR GÜNCELLEME
        duyurular_db = Duyuru.query.order_by(Duyuru.date_added.desc(), Duyuru.id.desc()).limit(5).all()
        
        duyuru_html = ""
        for d in duyurular_db:
            link = d.link if d.link else "#"
            duyuru_html += f'<li class="news-item"><a href="{link}">{d.title}</a></li>\\n'
            
        if not duyuru_html:
            duyuru_html = '<li class="news-item"><a href="#">İdareci ve Bürokratlar Birliği Derneği Web Sitesine Hoşgeldiniz...</a></li>'
            
        for file in ['anasayfa.html', 'index.html']:
            if os.path.exists(file):
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    s = bs4.BeautifulSoup(f.read(), 'lxml')
                    
                # Update duyurular
                duyuru_ul = s.find('ul', id='duyurular')
                if duyuru_ul:
                    duyuru_ul.clear()
                    duyuru_ul.append(bs4.BeautifulSoup(duyuru_html, 'html.parser'))
                    
                # Update slider
"""

code = code.replace("""
        for file in ['anasayfa.html', 'index.html']:
            if os.path.exists(file):
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    s = bs4.BeautifulSoup(f.read(), 'lxml')
                    
                # Update slider
""", injection)

# If it didn't find the loop because the original file didn't loop over ['anasayfa.html', 'index.html']
if 'for file in' not in code:
    code = code.replace("""
        # 1. Update anasayfa.html
        if os.path.exists('anasayfa.html'):
            with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
                soup = bs4.BeautifulSoup(f.read(), 'lxml')
""", """
        # DUYURULAR GÜNCELLEME
        duyurular_db = Duyuru.query.order_by(Duyuru.date_added.desc(), Duyuru.id.desc()).limit(10).all()
        
        duyuru_html = ""
        for d in duyurular_db:
            link = d.link if d.link else "#"
            duyuru_html += f'<li class="news-item"><a href="{link}">{d.title}</a></li>\\n'
            
        if not duyuru_html:
            duyuru_html = '<li class="news-item"><a href="#">İdareci ve Bürokratlar Birliği Derneği Web Sitesine Hoşgeldiniz...</a></li>'

        for file in ['anasayfa.html', 'index.html']:
            if os.path.exists(file):
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    soup = bs4.BeautifulSoup(f.read(), 'lxml')
                    
                # Update duyurular
                duyuru_ul = soup.find('ul', id='duyurular')
                if duyuru_ul:
                    duyuru_ul.clear()
                    duyuru_ul.append(bs4.BeautifulSoup(duyuru_html, 'html.parser'))
""")

    code = code.replace("""
            with open('anasayfa.html', 'w', encoding='utf-8') as f:
                f.write(str(soup))
        
        print("Updated anasayfa.html")
""", """
            with open(file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
        
        print("Updated anasayfa.html and index.html")
""")

with open('update_anasayfa.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated update_anasayfa.py!")
