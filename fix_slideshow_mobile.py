import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Add overflow: hidden and position: relative to #header so the absolute child is clipped properly
pattern_header = r'(#header\s*\{\s*background-color:\s*#ffffff;\s*\})'
repl_header = r'#header {\n    background-color: #ffffff;\n    overflow: hidden;\n    position: relative;\n}'
content = re.sub(pattern_header, repl_header, content)

# Remove the display: none !important for .slideshoww
pattern_slideshow_hide = r'\.slideshoww\s*\{\s*display:\s*none\s*!important;\s*/\*.*?\*/\s*\}'
content = re.sub(pattern_slideshow_hide, '', content)

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated style.css to show flags again and use overflow:hidden")
