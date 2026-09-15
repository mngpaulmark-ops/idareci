import re
with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    t = f.read()

t = re.sub(r'<a href="\{\{ url_for\(\'admin_menu\'\) \}\}" class="btn btn-dark m-1">.*?</a>', '<a href="{{ url_for(\'admin_menu\') }}" class="btn btn-dark m-1">Menü Ayarları</a>', t)
t = re.sub(r'<a href="\{\{ url_for\(\'admin_left_menu\'\) \}\}" class="btn btn-secondary m-1">.*?</a>', '<a href="{{ url_for(\'admin_left_menu\') }}" class="btn btn-secondary m-1">Sol Menü (Derneğimiz)</a>', t)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(t)
print('Fixed text')
