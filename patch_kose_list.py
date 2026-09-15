with open('templates/admin/kose_list.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("{{ yazi.date_added.strftime('%d.%m.%Y') }}", "{{ yazi.date_added.strftime('%d.%m.%Y') if yazi.date_added else '' }}")

with open('templates/admin/kose_list.html', 'w', encoding='utf-8') as f:
    f.write(text)
