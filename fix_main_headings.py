import os
import re

target_dir = r"C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org"

pages_to_restore = {
    'hakkimizda': 'Hakkımızda',
    'tuzugumuz': 'Tüzüğümüz',
    'yonetimkurulu': 'Yönetim Kurulu',
    'baskanlik-ve-birimler': 'Başkanlık ve Birimler',
    'yuksek-istisare-onur-kurulu-uyesi': 'Yüksek İstişare ve Onur Kurulu',
    'diger-kurullar': 'Diğer Kurullar',
    'temsilcilik': 'Temsilcilikler',
    'genclik-kollari': 'Gençlik Kolları',
    'uyelik': 'Üyelerimiz',
    'resimler': 'Fotoğraf Galerisi',
    'videolar': 'Video Galerisi',
    'duyurular': 'Duyurular',
    'etkinlik': 'Etkinlikler',
    'etkinlikler': 'Etkinlikler',
    'raporlar-belgeler': 'Raporlar / Belgeler'
}

for slug, title in pages_to_restore.items():
    filepath = os.path.join(target_dir, f"{slug}.html")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8', errors='surrogateescape') as f:
            html = f.read()

        # Find the main content area
        main_match = re.search(r'<div class="col-md-9" id="main">.*?<div class="panel-heading">([^<]+)</div>', html, flags=re.DOTALL)
        if main_match:
            # We found the heading inside main!
            old_heading = main_match.group(1)
            new_heading = f"İdareci ve Bürokratlar Birliği Derneği / {title}"
            
            # Replace only the first occurrence of this heading inside the main block
            # To be very safe, we replace the whole div match
            full_old_div = f'<div class="panel-heading">{old_heading}</div>'
            full_new_div = f'<div class="panel-heading">{new_heading}</div>'
            
            # Find the position of id="main"
            main_idx = html.find('id="main"')
            if main_idx != -1:
                # Replace the first panel-heading after main_idx
                before_main = html[:main_idx]
                after_main = html[main_idx:]
                
                after_main = after_main.replace(full_old_div, full_new_div, 1)
                new_html = before_main + after_main
                
                if new_html != html:
                    with open(filepath, 'w', encoding='utf-8', errors='surrogateescape') as f:
                        f.write(new_html)
                    print(f"Fixed title for {slug}.html -> {title}")
