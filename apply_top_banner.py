import glob, os, bs4

html_files = glob.glob('*.html') + glob.glob('haber/*.html')
count = 0

for f in html_files:
    if not os.path.isfile(f): continue
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            html = file.read()
    except:
        continue
        
    soup = bs4.BeautifulSoup(html, 'lxml')
    header_banner = soup.find('div', class_='header-banner')
    if not header_banner: continue
    
    # Remove old slideshoww
    slideshoww = header_banner.find('div', class_='slideshoww')
    if slideshoww:
        slideshoww.decompose()
        
    # Remove the old static top_banner if we already added one in previous iterations
    old_banner = header_banner.find('div', class_='top-banner-img')
    if old_banner:
        old_banner.decompose()
        
    col_12 = header_banner.find('div', class_='col-md-12')
    if not col_12: continue
    
    # Ensure the container is position relative if not already
    # Actually Bootstrap col-md-12 is relative. We can just add the div inside it.
    
    new_banner = bs4.BeautifulSoup(f'''
    <div class="top-banner-img" style="position:absolute; right: 0px; top: 0px; height: 155px; z-index: -90; max-width: 70%; overflow: hidden;">
        <img src="{"../" if "haber\\" in f or "haber/" in f else ""}themes/burokratlar/tema/images/top_banner.png" style="height: 100%; width: 100%; object-fit: contain; object-position: right;" alt="Biz Birlikte Gclyz">
    </div>
    ''', 'html.parser')
    
    col_12.append(new_banner)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    count += 1
    
print(f"Patched header in {count} HTML files.")
