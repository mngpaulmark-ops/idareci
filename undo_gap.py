import os
import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove the gap CSS block
css = re.sub(r'\n\n/\* Gap between galleries \*/\n\.photo-gallery \{\n    margin-bottom: 40px !important;\n\}\n', '', css)

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Gap CSS removed.")
