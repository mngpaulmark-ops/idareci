import os
import re

print("Fixing left menu links in all HTML files...")

count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root or 'instance' in root: continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='surrogateescape') as file:
                html = file.read()
            
            new_html = html
            # Replace Gençlik Kolları
            new_html = new_html.replace('href="./?mod=page&amp;id=5"', 'href="genclik-kollari.html"')
            
            # Replace Üyelerimiz (it has href="" just before Haberler)
            # Find: <li><a href="" target="_self"> oyelerimiz</a></li> or similar
            new_html = re.sub(r'href="([^"]*)"\s*target="_self">.\s*(?:oyelerimiz|Üyelerimiz)</a>', r'href="uyelik.html" target="_self"> oyelerimiz</a>', new_html)
            
            # Replace Duyurular
            new_html = re.sub(r'href="([^"]*)"\s*target="_self">.\s*Duyurular</a>', r'href="duyurular.html" target="_self"> Duyurular</a>', new_html)
            
            # Replace Raporlar / Belgeler
            new_html = re.sub(r'href="([^"]*)"\s*target="_self">.\s*Raporlar / Belgeler</a>', r'href="raporlar-belgeler.html" target="_self"> Raporlar / Belgeler</a>', new_html)
            
            if new_html != html:
                with open(path, 'w', encoding='utf-8', errors='surrogateescape') as file:
                    file.write(new_html)
                count += 1

print(f"Fixed left menu links in {count} HTML files!")
