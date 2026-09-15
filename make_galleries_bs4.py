import bs4, glob

images = glob.glob('data/haber/*.jpg')[:12]
img_tags = ''.join(['<div class="col-md-4 mb-4" style="margin-bottom:20px;"><a href="%s" class="fancybox" rel="gallery" title="Fotoğraf %d"><img src="%s" class="img-responsive rounded shadow gallery-hover" style="width:100%%; height:200px; object-fit:cover; border-radius:8px;"></a></div>' % (img.replace('\\', '/'), i+1, img.replace('\\', '/')) for i, img in enumerate(images)])

video_tags = ''.join(['<div class="col-md-6 mb-4" style="margin-bottom:20px;"><div class="gallery-hover shadow" style="background:#000; height:200px; display:flex; align-items:center; justify-content:center; color:white; font-size:40px; border-radius:8px; cursor:pointer;">&#9658;</div><h4 class="text-center mt-2" style="text-align:center;">Video %d</h4></div>' % (i+1) for i in range(4)])

def create_gallery(filename, title, content_tags):
    soup = bs4.BeautifulSoup(open('hakkimizda.html', encoding='utf-8', errors='ignore').read(), 'lxml')
    panels = soup.find_all('div', class_='panel')
    main_panel = None
    for p in panels:
        if 'Derne' in p.text or 'Kurul' in p.text or 'Hakk' in p.text:
            main_panel = p
            
    # Safest fallback: the last panel-body
    if not main_panel:
        main_panel = soup.find_all('div', class_='panel-body')[-1].parent

    heading = main_panel.find('div', class_='panel-heading')
    if heading:
        heading.string = title
    body = main_panel.find('div', class_='panel-body')
    if body:
        body.clear()
        row = soup.new_tag('div')
        row['class'] = 'row'
        body.append(row)
        new_content = bs4.BeautifulSoup(content_tags, 'html.parser')
        row.append(new_content)

    open(filename, 'w', encoding='utf-8').write(str(soup))

create_gallery('resimler.html', 'Fotoğraf Galerisi', img_tags)
create_gallery('videolar.html', 'Video Galerisi', video_tags)

for f in glob.glob('*.html'):
    c = open(f, encoding='utf-8', errors='ignore').read()
    if 'href="#" target="_self">Video Galerisi' in c:
        open(f, 'w', encoding='utf-8').write(c.replace('href="#" target="_self">Video Galerisi', 'href="videolar.html" target="_self">Video Galerisi'))

print("Galleries created successfully!")
