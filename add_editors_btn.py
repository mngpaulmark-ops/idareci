with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

replacement = 'Genel Ayarları</a>\n                    <a href="{{ url_for(\'admin_editors\') }}" class="btn btn-primary m-1">Yetki Ayarları (Editörler)</a>'
c = c.replace('Genel Ayarları</a>', replacement)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Added admin_editors to index.html")
