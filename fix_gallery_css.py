import os

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Only add if it doesn't already exist
if 'Custom Gallery Styles' not in css:
    css += '\n\n/* Custom Gallery Styles for Uniform Images */\n'
    css += '.fotogaleri.jcarousel ul li img,\n'
    css += '.videogaleri.jcarousel ul li img {\n'
    css += '    height: 130px !important;\n'
    css += '    width: 100% !important;\n'
    css += '    object-fit: cover !important;\n'
    css += '    border-radius: 4px;\n'
    css += '}\n'

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS appended.")
