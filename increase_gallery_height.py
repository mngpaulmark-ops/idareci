import re

with open('galeri_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Increase album thumbnail height to 400px
content = content.replace('height:280px;', 'height:400px;')

# Increase inner photo thumbnail height to 350px
content = content.replace('height:250px;', 'height:350px;')

with open('galeri_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated heights in galeri_helper.py")
