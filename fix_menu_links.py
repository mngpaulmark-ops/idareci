import re
import shutil
import os

files_to_update = ['anasayfa.html', 'hakkimizda.html']

for file in files_to_update:
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Fix Gençlik Kolları
        content = content.replace('href="./?mod=page&amp;id=5"', 'href="genclik-kollari.html"')
        content = content.replace('href="./?mod=page&id=5"', 'href="genclik-kollari.html"')
        
        # Fix Üyelerimiz
        content = content.replace('<a href="" target="_self">', '<a href="uyelik.html" target="_self">')
        
        # Fix Duyurular
        content = re.sub(r'<li><a href="#" target="_self">([^<]*Duyurular.*?)</a></li>', r'<li><a href="duyurular.html" target="_self">\1</a></li>', content)
        
        # Fix Raporlar
        content = re.sub(r'<li><a href="#" target="_self">([^<]*Raporlar.*?)</a></li>', r'<li><a href="raporlar-belgeler.html" target="_self">\1</a></li>', content)
        
        # Fix Haberler (Ensure it points to haberler.html)
        # Already points to haberler.html in the HTML we saw
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated links in {file}")
    except Exception as e:
        print(f"Error on {file}: {e}")

# Create missing files by copying hakkimizda.html
missing_files = ['genclik-kollari.html', 'duyurular.html', 'raporlar-belgeler.html', 'haberler.html']
for mfile in missing_files:
    if not os.path.exists(mfile):
        with open('hakkimizda.html', 'r', encoding='utf-8') as f:
            base = f.read()
            
        # Replace the main content with "Yapım aşamasında"
        pattern = r'(<div class="main">).*?(<div class="clearfix"></div>\s*</div>\s*</div>\s*<div class="clearfix">)'
        replacement = r'\1\n<div style="padding: 50px; text-align: center;"><h3>Sayfa Yapım Aşamasındadır</h3><p>İçerik en kısa sürede eklenecektir.</p></div>\n\2'
        new_base = re.sub(pattern, replacement, base, flags=re.DOTALL)
        
        # We need to make sure the regex matched.
        if new_base == base:
            # Fallback regex if above didn't match
            pattern2 = r'(<div class="col-md-9" id="main">).*?(<div class="clearfix"></div>\s*</div>)'
            replacement2 = r'\1\n<div class="main"><div style="padding: 50px; text-align: center;"><h3>Sayfa Yapım Aşamasındadır</h3><p>İçerik en kısa sürede eklenecektir.</p></div></div>\n\2'
            new_base = re.sub(pattern2, replacement2, base, flags=re.DOTALL)
            
        with open(mfile, 'w', encoding='utf-8') as f:
            f.write(new_base)
        print(f"Created {mfile}")
