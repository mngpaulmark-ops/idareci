import re

with open('galeri_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Change album list to 2 columns (col-md-6) and 350px height
content = content.replace('class="col-md-3 mb-4"', 'class="col-md-6 mb-4"')
content = content.replace('height:200px !important;', 'height:350px !important;')

# Change inner photos to 2 columns and 300px height
content = content.replace('class="col-md-3 col-sm-4 col-xs-6"', 'class="col-md-6 col-sm-6 col-xs-12"')
content = content.replace('height:150px !important;', 'height:300px !important;')

with open('galeri_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated galeri_helper.py for 2 columns and balanced height.")
