import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'\.whitebg\s*\{\s*background-color:\s*#ffffff;\s*padding-top:\s*15px;\s*\}'
replacement = '''.whitebg {
    background-color: #ffffff;
    padding-top: 15px;
    padding-bottom: 40px;
    min-height: 75vh;
}'''

new_content = re.sub(pattern, replacement, content)

# Fallback if pattern didn't match
if new_content == content:
    new_content += '\n.whitebg { padding-bottom: 40px; min-height: 75vh; }\n'

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated .whitebg with min-height and padding-bottom")
