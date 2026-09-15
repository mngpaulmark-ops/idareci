import glob
import os
from bs4 import BeautifulSoup

css_content = """
body { font-family: 'Roboto', sans-serif; background-color: #f8fafc; }
h1, h2, h3, h4, h5, h6, .panel-heading { font-family: 'Inter', sans-serif; }
.panel-primary > .panel-heading { background-color: #0f2b48; border-color: #0f2b48; }
.panel-kurumsal { border: 1px solid #e2e8f0; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); overflow: hidden; margin-bottom: 1.5rem; background: white;}
.btn-primary { background-color: #0f2b48; border-color: #0f2b48; border-radius: 0.25rem; transition: all 0.3s;}
.btn-primary:hover { background-color: #800000; border-color: #800000; }
.links a, #left-menu a { color: #0f2b48; text-decoration: none; }
.links a:hover, #left-menu a:hover { color: #800000; }
.main .box img { border-radius: 0.5rem; max-width: 100%; height: auto; }
"""

with open('kurumsal.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

js_code = """
<script id="dynamic-menu-script">
document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/menu')
        .then(response => response.json())
        .then(data => {
            // Update Top Menu
            var dropdowns = document.querySelectorAll('a.dropdown-toggle');
            dropdowns.forEach(function(el) {
                if (el.textContent.includes('Derneğimiz')) {
                    var ul = el.nextElementSibling;
                    if (ul && ul.tagName === 'UL') {
                        ul.innerHTML = '';
                        data.forEach(function(item) {
                            ul.innerHTML += '<li><a href="/dernegimiz/' + item.slug + '" target="_self">' + item.title + '</a></li>';
                        });
                        ul.innerHTML += '<li><a href="#" target="_self">Üyelerimiz</a></li>';
                    }
                }
            });
            // Update Left Menu
            var leftMenu = document.getElementById('left-menu');
            if (leftMenu) {
                leftMenu.innerHTML = '';
                data.forEach(function(item) {
                    leftMenu.innerHTML += '<li><a href="/dernegimiz/' + item.slug + '" target="_self">» ' + item.title + '</a></li>';
                });
                var otherItems = [
                    {title: 'Projeler', link: '#'},
                    {title: 'Gençlik Kolları', link: 'index-1.htm?mod=page&id=5'},
                    {title: 'Üyelerimiz', link: ''},
                    {title: 'Haberler', link: 'haber-listesi-1.html'},
                    {title: 'Duyurular', link: ''},
                    {title: 'Etkinlikler', link: 'etkinlikler.html'},
                    {title: 'Raporlar / Belgeler', link: ''},
                    {title: 'Fotoğraf Galerisi', link: 'resimler.html'}
                ];
                otherItems.forEach(function(item) {
                    leftMenu.innerHTML += '<li><a href="' + item.link + '" target="_self">» ' + item.title + '</a></li>';
                });
            }
        });
});
</script>
"""

files = glob.glob("*.html") + glob.glob("*.htm")

for filepath in files:
    if filepath.startswith('temp_demo') or filepath.startswith('layout'): continue
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'lxml')
    
    # 1. Add Fonts and Tailwind and kurumsal.css
    head = soup.find('head')
    if head:
        if not soup.find('link', href='kurumsal.css'):
            head.append(BeautifulSoup('<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">', 'lxml').link)
            head.append(BeautifulSoup('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Roboto:wght@400;500&display=swap" rel="stylesheet">', 'lxml').link)
            head.append(BeautifulSoup('<link href="kurumsal.css" rel="stylesheet">', 'lxml').link)
            
    # 2. Find and Replace Panels
    panels = soup.find_all('div', class_='panel')
    for panel in panels:
        heading = panel.find('div', class_='panel-heading')
        if not heading: continue
        heading_text = heading.get_text(strip=True).lower()
        
        # Remove Anket and Stat
        if 'anket' in heading_text or 'sayfa' in heading_text or 'istatislik' in heading_text:
            panel.decompose()
        # Replace Aidat
        elif 'aidat' in heading_text:
            new_panel = BeautifulSoup('''
            <div class="panel panel-kurumsal mb-4">
                <div class="panel-heading text-center font-bold" style="background:#0f2b48; color:white; padding: 10px;">Dijital İşlemler Portalı</div>
                <div class="panel-body text-center p-4">
                    <a href="uyelik.html" class="btn btn-primary w-full mb-2" style="background:#800000; border:none; display:block; padding:8px; color:white; border-radius:4px; text-decoration:none;">Üyelik Başvurusu</a>
                    <a href="#" class="btn btn-secondary w-full" style="background:#e2e8f0; display:block; padding:8px; color:#0f2b48; border-radius:4px; text-decoration:none;">Aidat Sorgulama</a>
                </div>
            </div>
            ''', 'lxml').div
            panel.replace_with(new_panel)
        # Add E-Bülten
        # Replace Etkinlik
        elif 'etkinlik' in heading_text:
            new_panel = BeautifulSoup('''
            <div class="panel panel-kurumsal mb-4">
                <div class="panel-heading text-center font-bold" style="background:#0f2b48; color:white; padding: 10px;">Gündem & Buluşmalar</div>
                <div class="panel-body p-4">
                    <ul class="list-none p-0 m-0 text-sm">
                        <li class="border-b py-2 mb-2"><span style="background:#800000; color:white; padding:2px 6px; border-radius:4px; font-size:12px;">Yakında</span> <a href="#" style="color:#0f2b48; font-weight:bold; text-decoration:none;">Politika Notu Yayını</a></li>
                        <li class="border-b py-2"><span style="background:#800000; color:white; padding:2px 6px; border-radius:4px; font-size:12px;">14 Mayıs</span> <a href="#" style="color:#0f2b48; font-weight:bold; text-decoration:none;">Dost Meclisi Buluşması</a></li>
                    </ul>
                </div>
            </div>
            <div class="panel panel-kurumsal mb-4">
                <div class="panel-heading text-center font-bold" style="background:#0f2b48; color:white; padding: 10px;">E-Bülten & Politika Notlarına Abone Olun</div>
                <div class="panel-body text-center p-4">
                    <input type="email" placeholder="E-Posta Adresiniz" class="form-control mb-2 p-2 border rounded w-full" style="width:100%; box-sizing:border-box;">
                    <button class="btn btn-primary w-full mt-2" style="background:#800000; border:none; padding:8px; color:white; border-radius:4px; width:100%;">Abone Ol</button>
                </div>
            </div>
            ''', 'lxml')
            panel.replace_with(new_panel)
        # Yazarlar
        elif 'yazar' in heading_text:
            heading.string = "Görüş & Politika Notları"
            
    # Also remove link-panel-cyan for Üyelik since we moved it to Digital Portal
    uyelik_link = soup.find('div', class_='link-panel-cyan')
    if uyelik_link:
        if 'üyelik' in uyelik_link.get_text(strip=True).lower() or 'uyelik' in uyelik_link.get_text(strip=True).lower():
            uyelik_link.decompose()
            
    # Remove hava durumu script block if present
    hava_script = soup.find(string=lambda t: t and 'hava_durumu' in t)
    if hava_script:
        if hava_script.parent.name == 'script':
            hava_script.parent.decompose()
            
    # Inject JS code before </body>
    body = soup.find('body')
    if body:
        # Check if already injected
        if not body.find('script', id='dynamic-menu-script'):
            js_soup = BeautifulSoup(js_code, 'lxml')
            body.append(js_soup.find('script'))
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print("Tüm sayfalara modern kurumsal UI başarıyla uygulandı!")
