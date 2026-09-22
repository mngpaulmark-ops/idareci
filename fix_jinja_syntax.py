with open('templates/admin/etkinlik_edit.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("\\'\\'", "''")

with open('templates/admin/etkinlik_edit.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed syntax error in HTML')
