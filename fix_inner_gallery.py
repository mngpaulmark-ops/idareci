import re

with open('galeri_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Revert the inner photos layout to 4 columns and 150px height
content = content.replace('class="col-md-6 col-sm-6 col-xs-12"', 'class="col-md-3 col-sm-4 col-xs-6"')
content = content.replace('height:300px !important;', 'height:150px !important;')

# Just to make absolutely sure, if I missed any:
content = content.replace('height:250px !important;', 'height:150px !important;')
content = content.replace('height:350px !important;', 'height:150px !important;')

with open('galeri_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Inner gallery photos resized to col-md-3 and 150px height for sharpness.")
