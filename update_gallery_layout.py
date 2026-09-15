import re

with open('galeri_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Change Album List (resimler.html)
content = content.replace('col-md-4 mb-4', 'col-md-6 mb-4')
content = content.replace('height:200px;', 'height:280px; font-size:16px;')

# Change Photos inside album (galeri-resimler-<id>.html)
content = content.replace('col-md-3 col-sm-4 col-xs-6', 'col-md-6 col-sm-6 col-xs-12')
content = content.replace('height:120px;', 'height:250px;')

with open('galeri_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated galeri_helper.py to display images in 2 columns and larger.")
