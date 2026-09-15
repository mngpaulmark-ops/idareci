import os
import re

count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root or 'instance' in root: continue
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='surrogateescape') as file:
                html = file.read()
            
            original = html
            html = re.sub(
                r'<div class="panel-heading">\s*<img[^>]+src="[^"]*icon-menu\.png"[^>]*>\s*Derne[^<]*</div>',
                '<div class="panel-heading">\n\t\t\t\t\t\t\t<img src="themes/burokratlar/tema/images/icon-menu.png" alt="Menu" /> Derneğimiz\n\t\t\t\t\t\t</div>',
                html
            )
            
            if html != original:
                with open(filepath, 'w', encoding='utf-8', errors='surrogateescape') as file:
                    file.write(html)
                count += 1

print(f"Fixed 'Derneğimiz' header in {count} HTML files!")
