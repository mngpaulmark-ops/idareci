import re

with open('templates/admin/haber_edit.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('name="file"', 'name="image"')

with open('templates/admin/haber_edit.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated template.")
