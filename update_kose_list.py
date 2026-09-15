with open('templates/admin/kose_list.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_button = '<a href="{{ url_for(\'admin_kose_edit\', id=yazi.id) }}" class="btn btn-sm btn-primary">Düzenle</a>\n                                    <form action="{{ url_for(\'admin_kose_sil\''
text = text.replace('<form action="{{ url_for(\'admin_kose_sil\'', new_button)

with open('templates/admin/kose_list.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated kose_list.html')
