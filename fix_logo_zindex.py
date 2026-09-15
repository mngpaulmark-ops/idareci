import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

logo_css = '''
/* Ensure the top logo is always in front of the flag/mosque background banner */
.header-banner .logo,
.header-banner a {
    position: relative;
    z-index: 5;
}
'''

if 'Ensure the top logo is always in front' not in content:
    content += '\n' + logo_css

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added z-index 5 and relative position to logo.")
