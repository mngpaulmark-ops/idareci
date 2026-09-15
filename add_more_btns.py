with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

replacement = 'Genel Ayarları</a>\n                    <a href="{{ url_for(\'admin_sidebar\') }}" class="btn btn-info m-1">Sağ Menü (Sidebar) Ayarları</a>\n                    <a href="{{ url_for(\'admin_videos\') }}" class="btn btn-dark m-1">Video Galeri Ayarları</a>'
c = c.replace('Genel Ayarları</a>', replacement)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Added sidebar and videos to index.html")
