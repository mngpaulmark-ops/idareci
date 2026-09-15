import re

file_path = r'themes/burokratlar/tema/css/style.css'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    css = f.read()

css = css.replace('.header-banner {\n\tbackground-color:#FFF !important;\n\toverflow: hidden;\n}', '.header-banner {\n\tbackground-color: transparent !important;\n\toverflow: visible;\n}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("style.css patched.")
