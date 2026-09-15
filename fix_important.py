import re

with open('galeri_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('height:400px;', 'height:400px !important;')
content = content.replace('height:350px;', 'height:350px !important;')

with open('galeri_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added !important to galeri_helper.py")
