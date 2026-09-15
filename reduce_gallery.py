import re

with open('galeri_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Revert Album List to smaller size
content = content.replace('col-md-6 mb-4', 'col-md-3 mb-4')
content = content.replace('height:400px !important;', 'height:200px !important;')

# 2. Revert Inner Photos to smaller size
content = content.replace('col-md-6 col-sm-6 col-xs-12', 'col-md-3 col-sm-4 col-xs-6')
content = content.replace('height:350px !important;', 'height:150px !important;')

# Just in case they were replaced without !important at some point:
content = content.replace('height:400px;', 'height:200px !important;')
content = content.replace('height:350px;', 'height:150px !important;')


with open('galeri_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated galeri_helper.py to reduce sizes by 50%.")
