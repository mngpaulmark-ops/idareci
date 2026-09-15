import os

with open('inject_hadith_final2.py', encoding='utf-8') as f:
    code = f.read()
    hadith_html = code.split('hadith_html = """\n')[1].split('"""')[0]

count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root or 'instance' in root: continue
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except:
                continue
            
            if 'daily-hadith' not in content and '<div class="basin">' in content:
                new_content = content.replace('<div class="basin">', hadith_html + '\n<div class="basin">', 1)
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                count += 1

print(f"Injected Hadith widget into {count} HTML files!")
