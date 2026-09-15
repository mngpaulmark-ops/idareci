import os
import re

base_dir = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org'
count = 0

for root, dirs, files in os.walk(base_dir):
    if '.git' in root or '__pycache__' in root or 'venv' in root: continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            
            if not content: continue
            
            new_content = re.sub(r'<meta[^>]*tuncer[^>]*>\n?', '', content, flags=re.IGNORECASE)
            new_content = re.sub(r'tuncer\s+Ǭnal', 'Yazar', new_content, flags=re.IGNORECASE)
            new_content = re.sub(r'tuncer\s+unal', 'Yazar', new_content, flags=re.IGNORECASE)
            new_content = re.sub(r'Tuncer\s+Ünal', 'Yazar', new_content, flags=re.IGNORECASE)
            
            if content != new_content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                count += 1

print(f"Cleaned {count} HTML files safely!")
