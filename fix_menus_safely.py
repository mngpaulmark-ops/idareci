import os
import re

perfect_menu = """<ul id="left-menu">
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

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='surrogateescape') as f:
        html = f.read()

    original_html = html
    # 1. Replace the entire left-menu ul block
    html = re.sub(r'<ul id="left-menu">.*?</ul>', perfect_menu, html, flags=re.DOTALL)
    
    # 2. Fix the "Derneğimiz" header above the left menu
    # In the backup it looks like:
    # <div class="panel-heading">
    # 						<img src="themes/burokratlar/tema/images/icon-menu.png" alt="Menu" /> Derneimiz
    # 						</div>
    # Let's replace the heading content
    html = re.sub(
        r'<div class="panel-heading">\s*<img[^>]+src="[^"]*icon-menu\.png"[^>]*>\s*Derne[^<]*</div>',
        '<div class="panel-heading">\n\t\t\t\t\t\t\t<img src="themes/burokratlar/tema/images/icon-menu.png" alt="Menu" /> Derneğimiz\n\t\t\t\t\t\t</div>',
        html
    )
    
    # 3. Fix the panel heading title in the main content area
    # Example: <div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Hakkımızda</div>
    # We will regex replace known bad titles
    # "dareci ve BǬrokratlar BirliYi DerneYi" or "dareci ve Brokratlar Birlii Dernei" -> İdareci ve Bürokratlar Birliği Derneği
    
    # Let's just find the panel heading inside col-md-9 id="main"
    # Actually, simpler: replace the specific bad strings in panel headings.
    html = re.sub(r'<div class="panel-heading">.*? / Hakk.*?</div>', '<div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Hakkımızda</div>', html)
    html = re.sub(r'<div class="panel-heading">.*? / Y.*?netim Kurulu</div>', '<div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Yönetim Kurulu</div>', html)
    html = re.sub(r'<div class="panel-heading">.*? / Ba.*?kanl.*?k ve Birimler</div>', '<div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Başkanlık ve Birimler</div>', html)
    html = re.sub(r'<div class="panel-heading">.*? / Y.*?ksek.*?Onur Kurulu</div>', '<div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Yüksek İstişare ve Onur Kurulu</div>', html)
    html = re.sub(r'<div class="panel-heading">.*? / Di.*?er Kurullar</div>', '<div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Diğer Kurullar</div>', html)
    html = re.sub(r'<div class="panel-heading">.*? / Temsilcilik.*?</div>', '<div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Temsilcilikler</div>', html)
    html = re.sub(r'<div class="panel-heading">.*? / Foto.*?raf Galerisi</div>', '<div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Fotoğraf Galerisi</div>', html)
    html = re.sub(r'<div class="panel-heading">.*? / Video Galerisi</div>', '<div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Video Galerisi</div>', html)
    html = re.sub(r'<div class="panel-heading">.*? / T.*?z.*?z</div>', '<div class="panel-heading">İdareci ve Bürokratlar Birliği Derneği / Tüzüğümüz</div>', html)
    
    if html != original_html:
        with open(filepath, 'w', encoding='utf-8', errors='surrogateescape') as f:
            f.write(html)
        return True
    return False

count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root or 'instance' in root: continue
    for f in files:
        if f.endswith('.html'):
            if fix_html_file(os.path.join(root, f)):
                count += 1
                
print(f"Fixed {count} HTML files safely!")
