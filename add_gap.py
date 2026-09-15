import os

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if 'Gap between galleries' not in css:
    css += '\n\n/* Gap between galleries */\n'
    css += '.photo-gallery {\n'
    css += '    margin-bottom: 40px !important;\n'
    css += '}\n'
    
    with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Gap CSS appended.")
else:
    print("Already added.")
