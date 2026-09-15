import os
import re

perfect_menu = """<ul id="left-menu">
    <li><a href="hakkimizda.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Hakkımızda</a></li>
    <li><a href="yonetimkurulu.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Yönetim Kurulu</a></li>
    <li><a href="baskanlik-ve-birimler.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Başkanlık ve Birimler</a></li>
    <li><a href="yuksek-istisare-onur-kurulu-uyesi.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Yüksek İstişare ve Onur Kurulu</a></li>
    <li><a href="diger-kurullar.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Diğer Kurullar</a></li>
    <li><a href="temsilcilik.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Temsilcilikler</a></li>
    <li><a href="genclik-kollari.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Gençlik Kolları</a></li>
    <li><a href="uyelik.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Üyelerimiz</a></li>
    <li><a href="haber-listesi.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Haberler</a></li>
    <li><a href="duyurular.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Duyurular</a></li>
    <li><a href="etkinlik.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Etkinlikler</a></li>
    <li><a href="raporlar-belgeler.html" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> Raporlar / Belgeler</a></li>
</ul>"""

count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root or 'instance' in root: continue
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='surrogateescape') as file:
                html = file.read()
            
            original = html
            html = re.sub(r'<ul id="left-menu">.*?</ul>', perfect_menu, html, flags=re.DOTALL)
            
            if html != original:
                with open(filepath, 'w', encoding='utf-8', errors='surrogateescape') as file:
                    file.write(html)
                count += 1
                
print(f"Replaced left menu safely in {count} HTML files!")
