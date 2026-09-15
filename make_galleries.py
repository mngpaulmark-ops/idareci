import os, glob
html = open('anasayfa.html', encoding='utf-8').read()
left_part = html.split('<div class="col-md-9 col-sm-9 col-xs-12">')[0] if '<div class="col-md-9 col-sm-9 col-xs-12">' in html else ''
right_part = html.split('<!-- sag tab -->')[1] if '<!-- sag tab -->' in html else ''

images = glob.glob('data/haber/*.jpg')[:12]
img_tags = ''.join(['<div class="col-md-4" style="margin-bottom:20px;"><img src="%s" style="width:100%%; height:200px; object-fit:cover; border-radius:8px;"></div>' % img.replace('\\', '/') for img in images])
gallery_html = left_part + '<div class="col-md-9 col-sm-9 col-xs-12"><div class="panel panel-kurumsal"><div class="panel-heading" style="background:#0f2b48; color:white; padding:10px; font-weight:bold;">Fotoğraf Galerisi</div><div class="panel-body"><div class="row">' + img_tags + '</div></div></div></div><!-- sag tab -->' + right_part

video_tags = ''.join(['<div class="col-md-6" style="margin-bottom:20px;"><div style="background:#000; height:200px; display:flex; align-items:center; justify-content:center; color:white; font-size:40px; border-radius:8px; cursor:pointer;">&#9658;</div><h4 style="text-align:center; margin-top:10px;">Video %d</h4></div>' % (i+1) for i in range(4)])
video_html = left_part + '<div class="col-md-9 col-sm-9 col-xs-12"><div class="panel panel-kurumsal"><div class="panel-heading" style="background:#0f2b48; color:white; padding:10px; font-weight:bold;">Video Galerisi</div><div class="panel-body"><div class="row">' + video_tags + '</div></div></div></div><!-- sag tab -->' + right_part

if left_part and right_part:
    open('resimler.html', 'w', encoding='utf-8').write(gallery_html)
    open('videolar.html', 'w', encoding='utf-8').write(video_html)

for f in glob.glob('*.html'):
    c = open(f, encoding='utf-8', errors='ignore').read()
    if 'href="#" target="_self">Video Galerisi' in c:
        open(f, 'w', encoding='utf-8').write(c.replace('href="#" target="_self">Video Galerisi', 'href="videolar.html" target="_self">Video Galerisi'))
print("Galleries generated!")
