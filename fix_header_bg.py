import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Add background-color: #ffffff to #header
if '#header {' not in content:
    content += '\n\n#header {\n    background-color: #ffffff;\n}\n'

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added #header { background-color: #ffffff; }")
