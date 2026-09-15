with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

btn = '<a href="{{ url_for(\'admin_left_menu\') }}" class="btn btn-secondary m-1">Sol Menü (Derneğimiz)</a>'
target = '<a href="{{ url_for(\'admin_menu\') }}" class="btn btn-dark m-1">'

if target in text:
    text = text.replace(target, target + '\n                    ' + btn + '\n')
    with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added button to index.html')
else:
    print('Target not found in index.html')
