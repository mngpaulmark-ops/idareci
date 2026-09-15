with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

replacement = 'Genel Ayarları</a>\n                    <a href="{{ url_for(\'admin_widgets\') }}" class="btn btn-secondary m-1">Ön Widget Ayarları</a>'
c = c.replace('Genel Ayarları</a>', replacement)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Added admin_widgets to index.html")
